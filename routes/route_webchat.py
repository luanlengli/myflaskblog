from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    session,
)
from flask_socketio import (
    emit,
    join_room,
    leave_room,
    SocketIO,
)

main = Blueprint('webchat', __name__)
socketio = SocketIO()


@main.route('/webchat')
def webchat_index():
    return render_template('webchat/webchat_index.html')


@main.route('/webchat/enter', methods=['POST'])
def webchat_enter():
    """
    加入聊天室, name 保存在 session 里面
    """
    name = request.form.get('name')
    if name is not None:
        session['name'] = name
        return redirect(url_for('.webchat_room'))
    else:
        return redirect(url_for('.webchat_index'))


@main.route('/webchat/room')
def webchat_room():
    name = session.get('name', '')
    if name == '':
        return redirect(url_for('.webchat_index'))
    else:
        return render_template('webchat/webchat_room.html')


@socketio.on('join', namespace="/webchat/room")
def join(data):
    print('join', data)
    room = data['room']
    join_room(room)
    session['room'] = room
    name = session.get('name')
    message = '用户:({}) 进入了房间'.format(name)
    d = dict(
        message=message,
    )
    emit('status', d, room=room)


@socketio.on('send', namespace="/webchat/room")
def send(data):
    name = session.get('name')
    message = data.get('message')
    formatted = '{} : {}'.format(name, message)
    print('send', formatted)
    d = dict(
        message=formatted
    )
    room = session.get('room')
    emit('message', d, room=room)


@socketio.on('leave', namespace="/webchat/room")
def leave(data):
    room = session.get('room')
    leave_room(room)
    name = session.get('name')
    d = dict(
        message='{} 离开了房间'.format(name),
    )
    emit('status', d, room=room)

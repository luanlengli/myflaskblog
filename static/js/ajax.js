var log = console.log.bind(console)

var e = function(selector, parent=document) {
    return parent.querySelector(selector)
}

/*
 ajax 函数
*/
var ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            log('load ajax response', r.response)
            var json = JSON.parse(r.response)
            responseCallback(json)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    log('ajax发送请求', method, data)
    // 发送请求
    r.send(data)
}


// Weibo API
// 获取所有 weibo
var apiWeiboAll = function (callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
    //    r = ajax('GET', path, '', callback)
    //    callback(r)
}

var apiWeiboAdd = function (form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}


var apiWeiboDelete = function (weibo_id, callback) {
    var path = `/api/weibo/delete?id=${weibo_id}`
    ajax('GET', path, '', callback)
}


var apiWeiboUpdate = function (form, callback) {
    var path = '/api/weibo/update'
    ajax('POST', path, form, callback)
}

// WeiboComment API
// 获取所有 WeiboComment
var apiCommentAll = function (weibo_id, callback) {
    var path = '/api/weibo_comment/all'
    var form = {
        weibo_id: weibo_id
    }
    ajax('POST', path, form, callback)
    //    r = ajax('GET', path, '', callback)
    //    callback(r)
}

var apiCommentAdd = function (form, callback) {
    var path = '/api/weibo_comment/add'
    ajax('POST', path, form, callback)
}


var apiCommentUpdate = function (form, callback) {
    var path = '/api/weibo_comment/update'
    ajax('POST', path, form, callback)
}


var apiCommentDelete = function (commentId, callback) {
    var path = `/api/weibo_comment/delete?id=${commentId}`
    ajax('GET', path, '', callback)
}

// Weibo模板
var weiboTemplate = function (weibo) {
    // WEIBO DOM
    var content = weibo.content
    var id = weibo.id
    var userId = weibo.user_id
    log('weiboTemplate userId =', userId)
    var t = `
    <p>
        <div class="weibo-cell" data-id=${id}>
            <span>微博:   </span>
            <span class="weibo-content">${content}</span>
            <span>from ${weibo.username}</span>
            <br>
            <button class="weibo-delete">删除</button>
            <button class="weibo-edit">编辑</button>
            <br>
            <input class="comment-input" id="id-comment-input-${id}">
            <button class="comment-add"">添加评论</button>
            <div class="comment-list" id="weibo-${id}">
            <span>评论</span>
            <br>
            </div>
        </div>
    </p>
    `
    return t
}

// Weibo更新模板
var weiboUpdateTemplate = function (title) {
    // WEIBO DOM
    var t = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${title}">
            <button class="weibo-update">更新</button>
        </div>
    `
    return t
}

// WeiboComment模板
var commentTemplate = function (comment) {
    log('run commentTemplate', comment)
    log('comment.weibo_id =', comment.weibo_id)
    log('comment.comment =', comment.content)
    log('comment.user_id =', comment.user_id)
    var t = `
        <div class="comment-cell" data-id=${comment.id}>
            <span>ID=${comment.id}</span>
            <span class='comment-content'>${comment.content}</span>
            <span> from ${comment.username}</span>
            <button class="comment-edit">编辑评论</button>
            <button class="comment-delete">删除评论</button>
            <br>
        </div>
    `
    return t
}

// WeiboComment更新模板
var CommentUpdateTemplate = function (content) {
    // WEIBO DOM
    var t = `
        <div class="comment-update-form">
            <input class="comment-update-input" value="${content}">
            <button class="comment-update">更新评论</button>
        </div>
    `
    return t
}

// 调用AJAX加载Weibo数据
var loadWeibos = function () {
    // 调用 ajax api 来载入数据
    // weibos = api_weibo_all()
    // process_weibos(weibos)
    apiWeiboAll(function (weibos) {
        log('load all weibos', weibos)
        // 循环添加到页面中
        for (var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo)
            log('weibo_id = ', weibo.id)
            weiboId = weibo.id
            loadComments(weiboId = weiboId)
        }
    })
}

// 调用AJAX插入Weibo数据
var insertWeibo = function (weibo) {
    var weiboCell = weiboTemplate(weibo)
    // 插入 weibo-list
    var weiboList = e('.weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

// 调用AJAX插入Weibo更新
var insertUpdateForm = function (title, weiboCell) {
    var updateForm = weiboUpdateTemplate(title)
    weiboCell.insertAdjacentHTML('afterBegin', updateForm)
}

// 调用AJAX加载WeiboComment数据
var loadComments = function (weiboId) {
    apiCommentAll(weibo_id = weiboId, function (comments) {
        for (var i = 0; i < comments.length; i++) {
            var comment = comments[i]
            log('loadcomments,', comment)
            insertComment(weiboId, comment)
        }
    })
}

// 调用AJAX插入WeiboComment数据
var insertComment = function (weiboId, comment) {
    log('run insertComment', comment)
    var commentCell = commentTemplate(comment)
    // 插入 comment-list
    var commentLocate = '#weibo-' + weiboId
    var commentList = e(commentLocate)
    log('insertComment commentList =', commentList)
    commentList.insertAdjacentHTML('beforeend', commentCell)
}

// 调用AJAX插入WeiboComment更新模板
var insertCommentUpdateForm = function (content, weiboCell) {
    var updateForm = CommentUpdateTemplate(content)
    weiboCell.insertAdjacentHTML('beforeend', updateForm)
}


//
// 绑定事件
//
var bindEventWeiboAdd = function () {
    var b = e('#id-button-add')
    b.addEventListener('click', function () {
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function (weibo) {
            // 收到返回的数据, 插入到页面中
            insertWeibo(weibo)
        })
    })
}


var bindEventWeiboDelete = function () {
    var weiboList = e('.weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function (event) {
        log(event)
        // 我们可以通过 event.target 来得到被点击的对象
        var self = event.target
        log('被点击的元素', self)
        // 通过比较被点击元素的 class
        // 来判断元素是否是我们想要的
        // classList 属性保存了元素所有的 class
        log(self.classList)
        if (self.classList.contains('weibo-delete')) {
            log('点到了删除按钮')
            weiboId = self.parentElement.dataset['id']
            apiWeiboDelete(weiboId, function (r) {
                log('apiWeiboDelete', r.message)
                // 删除 self 的父节点
                self.parentElement.remove()
                alert(r.message)
            })
        } else {
            log('点到了 weibo cell')
        }
    })
}


var bindEventWeiboEdit = function () {
    var weiboList = e('.weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function (event) {
        log(event)
        // 我们可以通过 event.target 来得到被点击的对象
        var self = event.target
        log('被点击的元素', self)
        // 通过比较被点击元素的 class
        // 来判断元素是否是我们想要的
        // classList 属性保存了元素所有的 class
        log(self.classList)
        if (self.classList.contains('weibo-edit')) {
            log('点到了编辑按钮')
            weiboCell = self.closest('.weibo-cell')
            log('self.closest(".weibo-cell") = ', weiboCell)
            weiboId = weiboCell.dataset['id']
            log("weiboCell.dataset['id'] = ", weiboCell)
            var weiboSpan = e('.weibo-content', weiboCell)
            log("e('.weibo-title', weiboCell) = ", weiboSpan)
            var title = weiboSpan.innerText
            log("weiboSpan.innerText = ", title)
            // 插入编辑输入框
            insertUpdateForm(title, weiboCell)
        } else {
            log('点到了 weibo cell')
        }
    })
}


var bindEventWeiboUpdate = function () {
    var weiboList = e('.weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function (event) {
        log(event)
        // 我们可以通过 event.target 来得到被点击的对象
        var self = event.target
        log('被点击的元素', self)
        // 通过比较被点击元素的 class
        // 来判断元素是否是我们想要的
        // classList 属性保存了元素所有的 class
        log(self.classList)
        if (self.classList.contains('weibo-update')) {
            log('点到了更新按钮')
            weiboCell = self.closest('.weibo-cell')
            weiboId = weiboCell.dataset['id']
            log('update weibo id', weiboId)
            input = e('.weibo-update-input', weiboCell)
            title = input.value
            var form = {
                id: weiboId,
                content: title,
            }

            apiWeiboUpdate(form, function (weibo) {
                // 收到返回的数据, 插入到页面中
                log('apiWeiboUpdate', weibo)

                var weiboSpan = e('.weibo-content', weiboCell)
                weiboSpan.innerText = weibo.content

                var updateForm = e('.weibo-update-form', weiboCell)
                updateForm.remove()
            })
        } else {
            log('点到了 weibo cell')
        }
    })
}


var bindEventCommentAdd = function () {
    var b = e('.weibo-list')
    log('bindEventCommentAdd ', b)
    //注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function (event) {
        self = event.target
        log('bindEventCommentAdd self.classList =', self.classList)
        if (self.classList.contains('comment-add')) {
            log('点击到添加评论')
            var weiboCell = self.closest('.weibo-cell')
            var weiboId = weiboCell.dataset['id']
            log('微博ID =', weiboId)
            var input = e('.comment-input', weiboCell)
            var content = input.value
            log('输入框内容为', content)
            var form = {
                weibo_id: weiboId,
                content: content
            }
            apiCommentAdd(form, function (comment) {
                // 收到返回的数据, 插入到页面中
                log('返回的数据=', comment)
                var weiboId = comment['weibo_id']
                insertComment(weiboId, comment)
            })
        }

    })
}


var bindEventCommentEdit = function () {
    var b = e('.weibo-list')
    b.addEventListener('click', function (event) {
        self = event.target
        // log('bindEventCommentEdit self.classList = ', self.classList)
        if (self.classList.contains('comment-edit')) {
            log('点击到编辑评论')
            var weiboCell = self.closest('.weibo-cell')
            var weiboId = weiboCell.dataset['id']
            log('微博ID =', weiboId)
            var commentCell = self.closest('.comment-cell')
            log('commentCell =', commentCell)
            var commentSpan = e('.comment-content', commentCell)
            var content = commentSpan.innerText
            log('评论的值：', content)
            insertCommentUpdateForm(content, commentCell)
        }
    })
}


var bindEventCommentUpdate = function () {
    var b = e('.weibo-list')
    b.addEventListener('click', function (event) {
        self = event.target
        // log('bindEventCommentEdit self.classList = ', self.classList)
        if (self.classList.contains('comment-update')) {
            log('点击到更新评论')
            var weiboCell = self.closest('.weibo-cell')
            var weiboId = weiboCell.dataset['id']
            log('微博ID =', weiboId)
            var commentCell = self.closest('.comment-cell')
            log('commentCell =', commentCell)
            var commentId = commentCell.dataset['id']
            log('评论ID =', commentId)
            var input = e('.comment-update-input', commentCell)
            var content = input.value
            log('更新评论的值：', content)
            var form = {
                weibo_id: weiboId,
                content: content,
                id: commentId,
            }
            apiCommentUpdate(form, function (comment) {
                // 收到返回的数据, 插入到页面中
                log('apiCommentUpdate', comment)

                var commentSpan = e('.comment-content', commentCell)
                commentSpan.innerText = comment.content

                var updateForm = e('.comment-update-form', commentCell)
                updateForm.remove()
            })
        }
    })
}


var bindEventCommentDelete = function () {
    var b = e('.weibo-list')
    b.addEventListener('click', function (event) {
        self = event.target
        // log('bindEventCommentEdit self.classList = ', self.classList)
        if (self.classList.contains('comment-delete')) {
            log('点击到删除评论')
            var weiboCell = self.closest('.weibo-cell')
            var weiboId = weiboCell.dataset['id']
            log('微博ID =', weiboId)
            var commentCell = self.closest('.comment-cell')
            log('commentCell =', commentCell)
            var commentId = commentCell.dataset['id']
            log('评论ID =', commentId)
            var form = {
                id: commentId,
            }
            apiCommentDelete(commentId, function (r) {
                log('apiCommentoDelete', r.message)
                // 删除 self 的父节点
                self.parentElement.remove()
                alert(r.message)
            })
        }
    })
}

var bindEvents = function () {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventCommentAdd()
    bindEventCommentEdit()
    bindEventCommentUpdate()
    bindEventCommentDelete()
}


// 定义__main函数作为统一的入口
var __main = function () {
    bindEvents()
    loadWeibos()
}

__main()
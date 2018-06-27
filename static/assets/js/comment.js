/**
 * Created by root on 2018/6/27 0027.
 */

var blog_id  //全局变量blog_id

// 提交评论
$(".comment_button").on('click', function () {
    if ($(".commitCommentForm textarea").val().trim() != '' && $(".commitCommentForm textarea").val().trim() != undefined && $(".commitCommentForm textarea").val().trim() != null) {
        var data = $(".commitCommentForm").serialize()
        $.ajax({
            url: '/blog/commitComment/',
            type: 'post',
            data: data,
            success: function (result) {
                if (result.status) {
                     getComment()
                }
            }
        })
    } else {
        layer.msg("请正确填写评论内容")
    }
})

//回复框的隐藏与显示
$('.reply_button').on('click', function () {
    <!--找到当前元素的 class 类名为commitReplyForm 的兄弟元素-->
    var dom = $(this).siblings('.commitReplyForm')
    if (dom.is(':hidden')) {
        dom.show()
    } else {
        dom.hide()
    }
})

//提交回复
$('.commitReplyForm input[type="button"]').on('click', function () {
    var form = $(this).parent().parent().parent()
    var content = $(this).parent().parent().children('textarea')
    if (content == '' || content == undefined || content == 'null') {
        layer.msg('请将内容填写完整')
        return false
    }
    $(this).attr('disabled', 'disabled')
    var data = form.serialize();
    $.ajax({
        url: "/blog/commitComment/",
        data: data,
        type: 'POST',
        success: function (result) {
            if (result.status) {
                $(this).parent().parent().children('textarea').val("")
                $(this).removeAttr('disabled')
                form.hide()
                getComment()
            }
        },
        error: function () {

        }
    })
})

// 提交回复或提交评论后的获取评论
function getComment() {
    $.ajax({
        url: '/blog/getComment/' + blog_id,
        type: 'get',
        success: function (ret) {
            if (ret.status) {
                var dom = comment_tree(ret.data)
                $("#comment_view_area").html(dom)
            }
        },
        error: function () {

        }
    })
}


function comment_tree(comment_query_list) {
    var root_comment_html = ''
    $.each(comment_query_list, function (index, comment) {
        var html = '<div class="pui-comment pui-comment-avatar-left pui-unbordered"><div class="pui-comment-avatar">'
        html += '<img src="images/2.png" class="pui-img-circle pui-img-xs"/><p>' + comment.commentUser
        html += '</p></div>'
        html += '<div class="pui-comment-container"> <div class="pui-comment-main pui-comment-arrow-lt">'
        html += '<header class="pui-comment-header"><div class="pui-comment-title-right"> '
        html += '#' + index + 1 + '楼 <a href="javascript:;">赞(18)</a> <a href="javascript:;">反对(0)</a>'
        html += '</div>'
        html += '<div class="pui-comment-subtitle">评论于 ' + comment.commentDate
        html += '</div></header>'
        html += '<section class="pui-comment-content"> ' + comment.commentContent
        html += '</section>'
        html += '<div class="pui-comment-foot"><a href="javascript:;" class="reply_button">回复</a><a href="javascript:;">顶</a><a href="javascript:;">举报</a>'
        html += '<form action="" class="commitReplyForm" style="display: none;">'
        html += '<div class="pui-form-group">'
        html += '<textarea name="commentContent" class="pui-input-border-default"></textarea>'
        html += '<input value="' + comment.commentBlog + '" name="commentBlog" style="display: none">'
        html += '<input value="' + comment.id + '" name="reply" style="display: none">'
        html += '<div class="pui-form-group"><input type="button" value="提交" class="pui-btn pui-btn-primary comment_button"/></div>'
        html += '</div>'
        html += '</form>'
        html += '</div>'
        html += '</div>'

        html += recursion(comment.children, index + 1)

        html += '</div>'
        html += '</div>'

        root_comment_html += html

        return root_comment_html
    })


    function recursion(comment_reply_list, root_index) {
        var leaf_comment_html = '';
        $.each(comment_reply_list, function (index, reply) {
            var leaf_html = '<div class="pui-comment-reply"><div class="pui-comment pui-comment-avatar-left"><div class="pui-comment-arrow"><span></span></div><div class="pui-comment-avatar">'
            leaf_html += '<img src="images/3.jpg" class="pui-img-circle pui-img-xs"/><p>' + reply.commentUser
            leaf_html += '</p></div>'
            leaf_html += '<div class="pui-comment-container"> <header class="pui-comment-header"><div class="pui-comment-title-right">'
            leaf_html += '#' + root_index + '楼-' + index + 1 + '<a href="javascript:;">赞(1)</a> <a href="javascript:;">反对(18)</a>'
            leaf_html += '</div><div class="pui-comment-subtitle"><a href="javascript:;" class="pui-link">' + reply.reply_src_user + '</a> <span class="pui-comment-reply-time">回复于 ' + reply.commentDate + '</span></div></header>'
            leaf_html += '<section class="pui-comment-content"><blockquote> ' + reply.reply_src_content + ' </blockquote><p> ' + reply.commentContent + ' </p></section>'
            leaf_html += '<footer class="pui-comment-foot"><a href="javascript:;" class="reply_button" >回复</a><a href="">顶</a><a href="javascript:;">举报</a>'
            leaf_html += '<form action="" class="commitReplyForm" style="display: none;">'
            leaf_html += '<div class="pui-form-group">'
            leaf_html += '<textarea name="commentContent" class="pui-input-border-default"></textarea>'
            leaf_html += '<input value="' + reply.commentBlog + '" name="commentBlog" style="display: none">'
            leaf_html += '<input value="' + reply.id + '" name="reply" style="display: none">'
            leaf_html += '<div class="pui-form-group"><input type="button" value="提交" class="pui-btn pui-btn-primary comment_button"/></div>'
            leaf_html += '</div>'
            leaf_html += '</form>'
            leaf_html += '</footer>'
            leaf_html += '</div>'
            leaf_html += '</div>'
            leaf_html += '</div>'

            leaf_html += recursion(reply.children, root_index)

            leaf_comment_html += leaf_html

            return leaf_comment_html

        })
    }


}

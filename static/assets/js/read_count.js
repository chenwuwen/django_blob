/**
 * Created by root on 2018/6/26 0026.
 */

var is_to_bottom = false // 页面是否 滚动到底部

// $(window).scroll() 方法用于监听滚动条的滚动
// $(window).scrollTop() 用于计算窗口相对于滚动条顶部的偏移， $(window).height() 和 $(document).height() 分别表示当面窗口的高度和文档的高度。
// 当窗口相对于滚动条顶部的位置偏移（即页面滚动时滑出页面的文档高度）加上窗口高度等于整个文档的高度时，表示我们的页面滚动已经到了底部。
// 注：网页文件编写的时候一定要在网页文件开始申明DOCTYPE，比如 <!DOCTYPE html> ，否则，可能会引起解析问题。就拿这个例子来说，如果不申明该元素， $(window).height() 和 $(document).height() 拿到的高度可能就是一样的。

$(window).scroll(function () {
    // scroll at bottom
    if ($(window).scrollTop() + $(window).height() == $(document).height()) {
        // load data
        is_to_bottom = true
    }
});

var stay_time = 0; //停留时间
$(function () {
    setInterval("has_view()", 10 * 1000)  //每十秒执行一次 has_view()函数
})

function has_view() {
    stay_time++;   //每十秒 style_time 加1
    if (stay_time >= 6 && is_to_bottom) {   //如果页面停留时间超过一分钟,并且页面已经滚动到底部说明已浏览
        $.ajax({
            url:'blog/add_read_count',
            type:'get',
            success:function () {

            },
            error:function () {

            }
        })
    }
}
   
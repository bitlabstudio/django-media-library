function add_content($content, $element) {
    var height
       ,width
       ,$viewer_bg
       ,padding_top
       ,$body;

    $body = $('body');
    $viewer_bg = $('<div style="display: none;" class="viewerbg"></div>');

    if ($content.prop('tagName') === 'IFRAME') {

        height = window.innerHeight / 1.5;
        width = height * 16 / 9 + 32;

        if (width > window.innerWidth) {

            // if the width is too small to fit into the window width, e.g. in portrait orientation, recalculate the size

            width = window.innerWidth / 1.15;
            height = width * 9 / 16 + 32;
        }

        padding_top = (window.innerHeight - height) / 2;

        $content.attr('height', height);
        $content.attr('width', width);
    } else {

        height = window.innerHeight / 1.5;
        width = window.innerHeight / 1.15;
        padding_top = (window.innerHeight - height) / 2;

        if ($element.height() > $element.width()) {

            // image is portrait

            $content.css({
                'height': height
               ,'max-height': window.innerHeight
               ,'width': 'auto'
            });

        } else {

            // image is landscape

            $content.css({
                'width': width
               ,'max-width': window.innerWidth
               ,'height': 'auto'
            });

        }
    }

    $viewer_bg.append($content);
    $viewer_bg.css('padding-top', padding_top + 'px');
    $body.append($viewer_bg);
    $body.find('.viewerbg').fadeIn();

    $viewer_bg.on('click', function(){
        $(this).fadeOut(function(){
            $(this).remove();
        });
    });
}

function get_preview_image($element) {
    var url;

    url = 'https://vimeo.com/api/v2/video/' + $element.attr('data-video-id') + '.json';

    $.ajax({
        dataType: "jsonp",
        url: url,
        success: function(data){
            $element.find('img').attr('src', data[0].thumbnail_medium)
        }
    });
}

function open_image($element) {

    // opens the full image for the thumb

    var img_url
       ,$img;

    img_url = $element.attr('data-src');
    $img = $('<img src="' + img_url + '" alt="Image" />');

    add_content($img, $element);

}

function open_video($element) {

    // opens the preview image as a video

    var video_id
       ,video_url
       ,$iframe;

    video_id = $element.attr('data-video-id');
    video_url = ($element.attr('href').indexOf('youtube') !== -1) ? 'https://www.youtube.com/embed/' : '//player.vimeo.com/video/';

    $iframe = $('<iframe src="' + video_url + video_id + '" frameborder=0 allowfullscreen></iframe>');

    add_content($iframe, $element);

}

$(document).on('click', '[data-class="video"]', function(e) {

    // open the video viewer instead of following the link

    e.preventDefault();

    open_video($(this));

});

$(document).on('click', '[data-class="image"]', function(e) {

    // open the image viewer

    e.preventDefault();

    open_image($(this));

});

$(document).ready(function() {
    $('[data-class="image"]').css('cursor', 'pointer');

    $('[data-video-origin="vimeo"]').each(function() {
        get_preview_image($(this));
    });
});

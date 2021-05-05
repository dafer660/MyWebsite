
function filesize(elem){
    document.cookie = `filesize=${elem.files[0].size}`
}

function count_chars() {
    try {
        const myTextArea = document.getElementById('body');
        const remainingCharsText = document.getElementById('body_count');
        const MAX_CHARS = 250;
        myTextArea.maxLength = 250;

        myTextArea.addEventListener('input', () => {
            const remaining = MAX_CHARS - myTextArea.value.length;
            const color = remaining < MAX_CHARS * 0.1 ? 'red' : null;
            remainingCharsText.textContent = remaining + " characters remaining";
            remainingCharsText.style.color = color;
            }
        )
    }catch (e) {
        console.log(e.description)
    }
}

async function copyURL(element){
    let URL = document.getElementById(element).getAttribute('src');
    let protocol = window.location.protocol
    let host = window.location.host
    let fullURL = protocol + '//' + host + URL
    await navigator.clipboard.writeText(fullURL);
}

$('.image-uploaded').popover({
    trigger: 'focus',
    placement: 'top',
    animation: true,
    content: "Copied URL to clipboard"
    }).click(function (event){
        console.log("clicked")
        let pop = $(this)
    // show the popover
    pop.popover('show')

    // run the function on the right element
    let elem = $(event.currentTarget)[0].id;
    copyURL(elem)

    // timeout for the popover
    pop.on('shown.bs.popover', function (){
        setTimeout(function (){
            pop.popover('hide')
        }, 1000);
    })
});


$(document).ready(function () {

    $('form').on('upload', function(event) {
		event.preventDefault();
		let formData = new FormData($('form')[0]);

        $.ajax({
            // xhr : function (){
            //   let xhr = new window.XMLHttpRequest() ;
            //
            //   xhr.upload.addEventListener('progress', function (ev){
            //       if (ev.lengthComputable) {
            //           console.log('Bytes: ' + ev.loaded);
            //           console.log('Total Size: ' + ev.total);
            //           console.log('Percentage Uploaded: ' + (ev.loaded / ev.total))
            //
            //           let percent = Math.round((ev.loaded / ev.total) * 100);
            //
            //           $('#progressBar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
            //       }
            //   });
            //   return xhr;
            // },
            type : 'POST',
            url : '/upload_files',
            data: formData,
            processData: false,
            contentType: false,
            success : function (response) {
                if(response != 0){
                    $('#image-div').html(response)
                    $('#title').value(response['title'])
                    $('#description').value(response['description'])
                    $('#body').value(response['body'])
                    $('#tags').value(response['tags'])

                    // $("#img").attr('src', response['image_resp']);
                }else{
                    alert('file not uploaded');
                }
            }
        });
    });
});


// $(function() {
//     let timer = null;
//     let xhr = null;
//     $('.image-uploaded').click(
//         function(event) {
//             // mouse in event handler
//             let elem = $(event.currentTarget);
//             let img_id = elem[0].id
//             timer = setTimeout(function() {
//                 timer = null;
//                 xhr = $.ajax(
//                     '/image/' + img_id + '/popup').done(
//                         function(data) {
//                             xhr = null
//                             // create and display popup here
//                             elem.popover({
//                                 trigger: 'click',
//                                 placement: 'top',
//                                 html: true,
//                                 animation: false,
//                                 container: elem,
//                                 content: data
//                             }).popover('show');
//                         }
//                     );
//             }, 1000);
//         },
//         function(event) {
//             // mouse out event handler
//             let elem = $(event.currentTarget);
//             console.log(timer)
//             console.log(xhr)
//             if (timer) {
//                 clearTimeout(timer);
//                 timer = null;
//             }
//             else if (xhr) {
//                 xhr.abort();
//                 xhr = null;
//             }
//             else {
//                 // destroy popup here
//                 elem.popover('hide')
//             }
//         }
//     )
// });
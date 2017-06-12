$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();   
});

$('#commands').on('click', 'input[name="update"]', function(event){
    event.preventDefault();
    run_process('update');
});

$('#commands').on('click', 'input[name="wipe"]', function(event){
    event.preventDefault();
    console.log('data wipe btn');
    run_process('wipe');
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showmessages(msgs) {
    $('#messages').hide();
    $.each(msgs, function() {
        $.each(this, function(k, message) {
                console.log(message.status+ ": " + message.text)

                var status;
                if (message.status == 'error') {
                  status = 'danger';
                } else {
                  status = message.status;
                }
                $('#messages').append("<div class='alert alert-"+status+" alert-dismissable fade in'>"+
                  "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>"+message.text+"</div>").fadeIn();
        });
    });
}

function linkbuild(links) {
    var linkstring = "<td class='vert-align col-md-6'>"
    $.each(links, function(key, val) {
        link = "<a role='button' class='btn btn-default btn-xs' data-toggle='tooltip' title='"+val[1]+"' href='"+val[1]+"' target='_blank'>"+val[0]+"</a> "
        linkstring += link  
    });
  console.log(linkstring);
  return linkstring;
}

function modifydom(soft) {
    $('tbody > tr').empty();
    $('tbody').hide();
    $.each(soft, function(k, v) {
      linkstring = linkbuild(v.links);
      $('tbody').append("<tr><td class='vert-align'>"+
                  "<a href='http://samlab.ws/soft/"+v.url_key+"' target='_blank'>"+
                  v.name+"</a></td><td class='vert-align'>"+
                  v.version+"</td><td class='vert-align'>"+
                  v.upd_date+"</td>"+linkstring+"</td></tr>").fadeIn()
    });
}

function run_process(action) {
    var csrftoken = getCookie('csrftoken');
    var data = {};
    data['csrfmiddlewaretoken'] = csrftoken;
    data[action] = action;
    $.ajax({
        url: '/',
        type: 'POST',
        data: data,
        datatype: 'json',

        // handle a successful response
        success: function(json) {
            console.log(json); // log the returned json to the console
            msgs = json.pop();
            showmessages(msgs);
            // modifydom(json)
        },

        // handle a non-successful response
        error: function(xhr, errmsg, err) {
            $('#messages').append("<div class='alert alert-danger fade in'>Oops! We have encountered an error: "+errmsg+
                "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function message_error(obj) {
  var html = '';
  if (typeof (obj) === 'object') {
    html = '<ul>'
    $.each(obj, function (key, value) {
      html += '<li>' + key + ': ' + value + '</li>'
    });
    html += '</ul>'
  } else {
    html = '<p>' + obj + '</p>'
  }
  Swal.fire({
    title: 'Error!',
    html: html,
    icon: 'error',
  })
}

function alert_confirm(url, parameters, callback) {
  $.confirm({
    title: 'Confirm!',
    content: 'Simple confirm!',
    buttons: {
      info: {
        text: 'Confirm',
        btnClass: 'btn-primary',
        action: function () {
          $.ajax({
            url: url,
            type: 'POST',
            data: parameters,
            dataType: 'json',
            processData: false,
            contentType: false
          }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
              callback();
              return false;
            }
            message_error(data.error)
          }).fail(function (data) {
            alert('Error')
          }).always(function (data) {

          })
        },
      },
      danger: {
        text: 'Cancel',
        btnClass: 'btn-red',
        cancel: function () {
          $.alert('Canceled!');
        },
      }
    }
  });
}

function alert_delete_confirm(urls, parameter, callbacks) {
  $.confirm({
    title: 'Confirm!',
    content: 'Simple confirm!',
    buttons: {
      info: {
        text: 'Confirm',
        btnClass: 'btn-primary',
        action: function () {
          $.ajax({
            url: urls,
            type: 'POST',
            data: parameter,
            dataType: 'json'
          }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
              callbacks();
              return false;
            }
            message_error(data.error)
          }).fail(function (data) {
            alert('Error')
          }).always(function (data) {

          })
        },
      },
      danger: {
        text: 'Cancel',
        btnClass: 'btn-red',
        cancel: function () {
          $.alert('Canceled!');
        },
      }
    }
  });
}


'use strict'

const getDepartureTable = () => {
  return $.ajax({
    url: window.location.href,
    method: 'GET'
  })
}

window.setInterval(function () {
  getDepartureTable()
    .then(response => {
      $('.departure-container').html(response.table_html)
    })
}, 60000); // set the table html every 60 seconds.

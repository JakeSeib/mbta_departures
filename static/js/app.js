'use strict'

const url = djangoDebug === 'True' ? 'http://127.0.0.1:8000/' : 'http://ec2-18-224-137-245.us-east-2.compute.amazonaws.com/'

const getDepartureTable = () => {
  return $.ajax({
    url: url,
    method: 'GET'
  })
}

window.setInterval(function () {
  getDepartureTable()
    .then(response => {
      $('.departure-container').html(response.table_html)
    })
}, 60000); // set the table html every 60 seconds.

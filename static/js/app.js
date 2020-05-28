'use strict'

window.setTimeout(function () {
    location.href = "http://ec2-18-224-137-245.us-east-2.compute.amazonaws.com/";
}, 30000); // refresh/redirect after 30 seconds.

const testDjangoResponse = () => {
  return $.ajax({
    url: `http://127.0.0.1:8000/`,
    method: 'GET'
  })
}

console.log(testDjangoResponse())

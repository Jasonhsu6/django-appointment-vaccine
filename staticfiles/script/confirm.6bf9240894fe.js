//var today = new Date().toISOString().split('T')[0];
var yesterday = new Date();
yesterday.setDate(tomorrow.getDate() - 1)
document.getElementsByName("schedule_date")[0].setAttribute('min', yesterday.toISOString().split('T')[0]);
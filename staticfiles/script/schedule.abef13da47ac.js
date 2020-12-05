//var today = new Date().toISOString().split('T')[0];
var tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1)
document.getElementsByName("schedule_date")[0].setAttribute('min', tomorrow.toISOString().split('T')[0]);
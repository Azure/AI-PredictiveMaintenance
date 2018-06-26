function displayAlert(message, alertClass) {
    var alertNode = $($('#alert-template').html());
    alertNode.addClass(alertClass);
    alertNode.children().first().html(message);
    alertNode.appendTo($('#alert-container'));
}

function renderDate(dateAsString, iso=false) {
    if (!/Z$/.test(dateAsString)) {
        dateAsString += 'Z';
    }
    var utcDate = new Date(dateAsString);
    if (!iso) {
      return utcDate.toLocaleString();
    } else {
      var tzOffset = utcDate.getTimezoneOffset();
      var dateMs = utcDate.getTime();
      dateMs -= tzOffset * 60 * 1000;
      var localDate = new Date(dateMs);
      return localDate.toISOString();
    }
}

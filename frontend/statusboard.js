REALTIME_URL = "https://api.wheresthefuckingtrain.com/by-id/"
STATIC_URL = "http://localhost:5001/"
STATUS_URL = "http://localhost:5002/"
WEATHER_URL = "http://localhost:5003/"
CUT_OFF_MIN = 3
CUT_OFF_MAX = 20
SINCE_LAST_UPDATE = 300
subwayStatus = {};
errors = {}

function minutesAway(datetime) {
  diff = new Date(datetime) - new Date();
  seconds = diff / 1000;
  return Math.floor((((seconds % 31536000) % 86400) % 3600) / 60);
}

function secondsSinceUpdate(datetime) {
  diff = new Date - new Date(datetime)
  return diff / 1000
}

function getServiceStatus() {
  $.ajax({
    url: STATUS_URL,
    context: document.body,
    success: function(data) {
      subwayStatus = data;
    }
  });
}

function writeError(msg) {
  var template = $('#errorTemplate').html();
  Mustache.parse(template)
  var rendered = Mustache.render(template, {"error": msg});
  $('#errors').html(rendered);
}

function getRealTimeLine(subwayLine) {
  $.ajax({
    url: REALTIME_URL + subwayLine,
    context: document.body,
    success: function(data) {
      trips = new Array()
      if (data.data[0]['N'].length > 0) {
        for (var i=0; i<data.data[0]['N'].length; i++) {
          var minAway = Number(minutesAway(data.data[0]['N'][i]['time']));
          if (minAway < CUT_OFF_MIN) {
            continue
          }
          if (minAway > CUT_OFF_MAX) {
            continue
          }
          sinceLastUpdate = secondsSinceUpdate(data.updated);
          if (Number(sinceLastUpdate) > SINCE_LAST_UPDATE) {
            errors["realtime"] = "Realtime update since: " + sinceLastUpdate
          }
          var train = new Map();
          train['image'] = data.data[0]['N'][i]['route'] + ".svg";
          train['minutesAway'] = minAway
          trips.push(train);
        }
        if (trips.length > 0) {
          try {
            trips[0]['serviceStatus'] = subwayStatus.data['L'];
            errors["status_L"] = ""
          } catch (e) {
            errors["status_L"] = "Failed to get L status"
          }
        }
      }
      renderLine(subwayLine, trips);
    }
  });
}

function getStaticSchedule(subwayLine) {
  $.ajax({
    url: STATIC_URL + subwayLine,
    context: document.body,
    success: function(data) {
      if (data.data.length > 0) {
        trips = new Array()
        for (var i=0; i<data.data.length; i++) {
          var minAway = minutesAway(data.data[i]);
          if (minAway < CUT_OFF_MIN) {
            continue
          }
          if (minAway > CUT_OFF_MAX) {
            continue
          }
          var train = {};
          train['image'] = "G.svg";
          train['minutesAway'] =  minAway
          trips.push(train);
        }
        if (trips.length > 0) {
          try {
            trips[0]['serviceStatus'] = subwayStatus.data['G'];
            errors["status_G"] = ""
          } catch (e) {
            errors["status_G"] = "Failed to get G status"
          }
        }
        renderLine(subwayLine, trips);
      }
    }
  });
}

function renderLine(subwayLine, trips) {
  var template = $('#tripsTemplate').html();
  Mustache.parse(template)
  var rendered = Mustache.render(template, trips);
  $('#'+subwayLine).html(rendered);
}

function getCurrentWeather() {
  $.ajax({
    url: WEATHER_URL + "current",
    context: document.body,
    success: function(data) {
      var curTempObj = {};
      weather_icons = new Array();
      temp_max = data['main']['temp_max'];
      temp_min = data['main']['temp_min'];
      for (var i=0; i<data['weather'].length; i++) {
        weather_icons.push(data['weather'][i]['icon']);
      }
      curTempObj['current'] = data['main']['temp'];
      curTempObj['max'] = data['main']['temp_max'];
      curTempObj['min'] = data['main']['temp_min'];
      curTempObj['icons'] = weather_icons;
      renderCurrentTemp(curTempObj);
    }
  });
}

// function getForecastWeather() {
//   $.ajax({
//     url: WEATHER_URL + "forecast",
//     context: document.body,
//     success: function(data) {
//       console.log(data);
//     }
//   });
// }

function renderCurrentTemp(obj) {
  var template = $('#weatherTemplate').html();
  Mustache.parse(template)
  var rendered = Mustache.render(template, obj);
  $('#footer').html(rendered);
}

function checkForErrors() {
  msg = ""
  if (errors["status_G"]) {
    msg += errors["status_G"];
    msg += " "
  }
  if (errors["status_L"]) {
    msg += errors["status_L"];
    msg += " "
  }
  if (errors["realtime"]) {
    msg += errors["realtime"];
  }
  writeError(msg);
}

function getTrips() {
  getRealTimeLine("5194");
  getStaticSchedule("G30");
}

function clock() {
  document.getElementById("clock").innerHTML = new Date().toLocaleTimeString();
}

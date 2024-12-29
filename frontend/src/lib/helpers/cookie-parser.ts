

export class CookieParser {
  
    static getCookies = function () {
    var pairs = document.cookie.split(";");
    var cookies : {
        [key : string] : string
    } = {};
    for (var i = 0; i < pairs.length; i++) {
      var pair = pairs[i].split("=");
      cookies[(pair[0] + "").trim()] = unescape(pair.slice(1).join("="));
    }
    return cookies;
  };
}

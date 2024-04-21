

Date.prototype.format = function (format) {
	   var args = {
		   "M+": this.getMonth() + 1,
		   "d+": this.getDate(),
		   "h+": this.getHours(),
		   "m+": this.getMinutes(),
		   "s+": this.getSeconds(),
		   "q+": Math.floor((this.getMonth() + 3) / 3),  //quarter
		   "S": this.getMilliseconds()
	   };
	   if (/(y+)/.test(format))
		   format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
	   for (var i in args) {
		   var n = args[i];
		   if (new RegExp("(" + i + ")").test(format))
			   format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? n : ("00" + n).substr(("" + n).length));
	   }
	   return format;
};


//生成指定长度的随机数字字符
function randomString(length) {
      const str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
      let result = '';
      for(let i = 0; i<length; i++)
      {
        let id = Math.floor(Math.random() * str.length);
        result += str[id];
      }
      return result;
  }

// 获取当前时间
function NowTime() {
    var time = new Date();
    var year = time.getFullYear();// 获取年
    var month = time.getMonth() + 1;// 或者月
    var day = time.getDate();// 或者天
    var hour = time.getHours();// 获取小时
    var minu = time.getMinutes();// 获取分钟
    var second = time.getSeconds();// 或者秒
    var data = year + "-";
    if (month < 10) {
        data += "0";
    }
    data += month + "-";
    if (day < 10) {
        data += "0"
    }
    data += day + " ";
    if (hour < 10) {
        data += "0"
    }
    data += hour + ":";
    if (minu < 10) {
        data += "0"
    }
    data += minu + ":";
    if (second < 10) {
        data += "0"
    }
    data += second;
    return data;
}
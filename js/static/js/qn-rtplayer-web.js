! function(e, t) {
	"object" == typeof exports && "undefined" != typeof module ? t(exports) : "function" == typeof define && define
		.amd ? define(["exports"], t) : t((e = "undefined" != typeof globalThis ? globalThis : e || self)
			.QNRTPlayer = {})
}(this, (function(e) {
	"use strict";
	/*! *****************************************************************************
	    Copyright (c) Microsoft Corporation.

	    Permission to use, copy, modify, and/or distribute this software for any
	    purpose with or without fee is hereby granted.

	    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
	    REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
	    AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
	    INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
	    LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
	    OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
	    PERFORMANCE OF THIS SOFTWARE.
	    ***************************************************************************** */
	var t = function(e, r) {
		return (t = Object.setPrototypeOf || {
				__proto__: []
			}
			instanceof Array && function(e, t) {
				e.__proto__ = t
			} || function(e, t) {
				for (var r in t) Object.prototype.hasOwnProperty.call(t, r) && (e[r] = t[r])
			})(e, r)
	};

	function r(e, r) {
		function n() {
			this.constructor = e
		}
		t(e, r), e.prototype = null === r ? Object.create(r) : (n.prototype = r.prototype, new n)
	}
	var n = function() {
		return (n = Object.assign || function(e) {
			for (var t, r = 1, n = arguments.length; r < n; r++)
				for (var i in t = arguments[r]) Object.prototype.hasOwnProperty.call(t, i) && (e[
					i] = t[i]);
			return e
		}).apply(this, arguments)
	};

	function i(e, t, r, n) {
		return new(r || (r = Promise))((function(i, o) {
			function s(e) {
				try {
					c(n.next(e))
				} catch (e) {
					o(e)
				}
			}

			function a(e) {
				try {
					c(n.throw(e))
				} catch (e) {
					o(e)
				}
			}

			function c(e) {
				var t;
				e.done ? i(e.value) : (t = e.value, t instanceof r ? t : new r((function(e) {
					e(t)
				}))).then(s, a)
			}
			c((n = n.apply(e, t || [])).next())
		}))
	}

	function o(e, t) {
		var r, n, i, o, s = {
			label: 0,
			sent: function() {
				if (1 & i[0]) throw i[1];
				return i[1]
			},
			trys: [],
			ops: []
		};
		return o = {
			next: a(0),
			throw: a(1),
			return: a(2)
		}, "function" == typeof Symbol && (o[Symbol.iterator] = function() {
			return this
		}), o;

		function a(o) {
			return function(a) {
				return function(o) {
					if (r) throw new TypeError("Generator is already executing.");
					for (; s;) try {
						if (r = 1, n && (i = 2 & o[0] ? n.return : o[0] ? n.throw || ((i = n
								.return) && i.call(n), 0) : n.next) && !(i = i.call(n, o[1])).done)
							return i;
						switch (n = 0, i && (o = [2 & o[0], i.value]), o[0]) {
							case 0:
							case 1:
								i = o;
								break;
							case 4:
								return s.label++, {
									value: o[1],
									done: !1
								};
							case 5:
								s.label++, n = o[1], o = [0];
								continue;
							case 7:
								o = s.ops.pop(), s.trys.pop();
								continue;
							default:
								if (!(i = s.trys, (i = i.length > 0 && i[i.length - 1]) || 6 !== o[
										0] && 2 !== o[0])) {
									s = 0;
									continue
								}
								if (3 === o[0] && (!i || o[1] > i[0] && o[1] < i[3])) {
									s.label = o[1];
									break
								}
								if (6 === o[0] && s.label < i[1]) {
									s.label = i[1], i = o;
									break
								}
								if (i && s.label < i[2]) {
									s.label = i[2], s.ops.push(o);
									break
								}
								i[2] && s.ops.pop(), s.trys.pop();
								continue
						}
						o = t.call(e, s)
					} catch (e) {
						o = [6, e], n = 0
					} finally {
						r = i = 0
					}
					if (5 & o[0]) throw o[1];
					return {
						value: o[0] ? o[1] : void 0,
						done: !0
					}
				}([o, a])
			}
		}
	}

	function s(e) {
		return i(this, void 0, void 0, (function() {
			var t, r;
			return o(this, (function(n) {
				switch (n.label) {
					case 0:
						return t = {
							offerToReceiveAudio: !0,
							offerToReceiveVideo: !0
						}, [4, e.createOffer(t)];
					case 1:
						return (r = n.sent()).sdp ? [2, -1 !== r.sdp.toLowerCase()
							.indexOf("h264")
						] : [2, !1]
				}
			}))
		}))
	}

	function a() {
		return i(this, void 0, void 0, (function() {
			var e, t, r, n, i, a;
			return o(this, (function(o) {
				switch (o.label) {
					case 0:
						return (e = !!window.RTCPeerConnection) ? [4, s(t =
							new RTCPeerConnection)] : [2, {
							peerConnection: !1,
							H264: !1,
							getStats: !1
						}];
					case 1:
						return r = o.sent(), n = !!t.getStats, t.close(), [4, s(i =
							new RTCPeerConnection)];
					case 2:
						return a = o.sent(), i.close(), [2, {
							peerConnection: e,
							H264: r || a,
							getStats: n
						}]
				}
			}))
		}))
	}
	var c = "undefined" != typeof globalThis ? globalThis : "undefined" != typeof window ? window :
		"undefined" != typeof global ? global : "undefined" != typeof self ? self : {};

	function d(e) {
		var t = {
			exports: {}
		};
		return e(t, t.exports), t.exports
		/*!
		 * UAParser.js v0.7.23
		 * Lightweight JavaScript-based User-Agent string parser
		 * https://github.com/faisalman/ua-parser-js
		 *
		 * Copyright © 2012-2019 Faisal Salman <f@faisalman.com>
		 * Licensed under MIT License
		 */
	}
	var p = (new(d((function(e, t) {
			! function(r, n) {
				var i = "function",
					o = "object",
					s = "model",
					a = "name",
					c = "type",
					d = "vendor",
					p = "version",
					l = "architecture",
					u = "console",
					f = "mobile",
					h = "tablet",
					m = "smarttv",
					v = "wearable",
					g = {
						extend: function(e, t) {
							var r = {};
							for (var n in e) t[n] && t[n].length % 2 == 0 ? r[n] = t[n]
								.concat(e[n]) : r[n] = e[n];
							return r
						},
						has: function(e, t) {
							return "string" == typeof e && -1 !== t.toLowerCase().indexOf(e
								.toLowerCase())
						},
						lowerize: function(e) {
							return e.toLowerCase()
						},
						major: function(e) {
							return "string" == typeof e ? e.replace(/[^\d\.]/g, "").split(
								".")[0] : n
						},
						trim: function(e) {
							return e.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "")
						}
					},
					y = {
						rgx: function(e, t) {
							for (var r, s, a, c, d, p, l = 0; l < t.length && !d;) {
								var u = t[l],
									f = t[l + 1];
								for (r = s = 0; r < u.length && !d;)
									if (d = u[r++].exec(e))
										for (a = 0; a < f.length; a++) p = d[++s], typeof(
												c = f[a]) === o && c.length > 0 ? 2 == c
											.length ? typeof c[1] == i ? this[c[0]] = c[1]
											.call(this, p) : this[c[0]] = c[1] : 3 == c
											.length ? typeof c[1] !== i || c[1].exec && c[1]
											.test ? this[c[0]] = p ? p.replace(c[1], c[2]) :
											n : this[c[0]] = p ? c[1].call(this, p, c[2]) :
											n : 4 == c.length && (this[c[0]] = p ? c[3]
												.call(this, p.replace(c[1], c[2])) : n) :
											this[c] = p || n;
								l += 2
							}
						},
						str: function(e, t) {
							for (var r in t)
								if (typeof t[r] === o && t[r].length > 0) {
									for (var i = 0; i < t[r].length; i++)
										if (g.has(t[r][i], e)) return "?" === r ? n : r
								} else if (g.has(t[r], e)) return "?" === r ? n : r;
							return e
						}
					},
					w = {
						browser: {
							oldsafari: {
								version: {
									"1.0": "/8",
									1.2: "/1",
									1.3: "/3",
									"2.0": "/412",
									"2.0.2": "/416",
									"2.0.3": "/417",
									"2.0.4": "/419",
									"?": "/"
								}
							}
						},
						device: {
							amazon: {
								model: {
									"Fire Phone": ["SD", "KF"]
								}
							},
							sprint: {
								model: {
									"Evo Shift 4G": "7373KT"
								},
								vendor: {
									HTC: "APA",
									Sprint: "Sprint"
								}
							}
						},
						os: {
							windows: {
								version: {
									ME: "4.90",
									"NT 3.11": "NT3.51",
									"NT 4.0": "NT4.0",
									2e3: "NT 5.0",
									XP: ["NT 5.1", "NT 5.2"],
									Vista: "NT 6.0",
									7: "NT 6.1",
									8: "NT 6.2",
									8.1: "NT 6.3",
									10: ["NT 6.4", "NT 10.0"],
									RT: "ARM"
								}
							}
						}
					},
					T = {
						browser: [
							[/(opera\smini)\/([\w\.-]+)/i,
								/(opera\s[mobiletab]{3,6}).+version\/([\w\.-]+)/i,
								/(opera).+version\/([\w\.]+)/i, /(opera)[\/\s]+([\w\.]+)/i
							],
							[a, p],
							[/(opios)[\/\s]+([\w\.]+)/i],
							[
								[a, "Opera Mini"], p
							],
							[/\s(opr)\/([\w\.]+)/i],
							[
								[a, "Opera"], p
							],
							[/(kindle)\/([\w\.]+)/i,
								/(lunascape|maxthon|netfront|jasmine|blazer)[\/\s]?([\w\.]*)/i,
								/(avant\s|iemobile|slim)(?:browser)?[\/\s]?([\w\.]*)/i,
								/(bidubrowser|baidubrowser)[\/\s]?([\w\.]+)/i,
								/(?:ms|\()(ie)\s([\w\.]+)/i, /(rekonq)\/([\w\.]*)/i,
								/(chromium|flock|rockmelt|midori|epiphany|silk|skyfire|ovibrowser|bolt|iron|vivaldi|iridium|phantomjs|bowser|quark|qupzilla|falkon)\/([\w\.-]+)/i
							],
							[a, p],
							[/(konqueror)\/([\w\.]+)/i],
							[
								[a, "Konqueror"], p
							],
							[/(trident).+rv[:\s]([\w\.]{1,9}).+like\sgecko/i],
							[
								[a, "IE"], p
							],
							[/(edge|edgios|edga|edg)\/((\d+)?[\w\.]+)/i],
							[
								[a, "Edge"], p
							],
							[/(yabrowser)\/([\w\.]+)/i],
							[
								[a, "Yandex"], p
							],
							[/(Avast)\/([\w\.]+)/i],
							[
								[a, "Avast Secure Browser"], p
							],
							[/(AVG)\/([\w\.]+)/i],
							[
								[a, "AVG Secure Browser"], p
							],
							[/(puffin)\/([\w\.]+)/i],
							[
								[a, "Puffin"], p
							],
							[/(focus)\/([\w\.]+)/i],
							[
								[a, "Firefox Focus"], p
							],
							[/(opt)\/([\w\.]+)/i],
							[
								[a, "Opera Touch"], p
							],
							[/((?:[\s\/])uc?\s?browser|(?:juc.+)ucweb)[\/\s]?([\w\.]+)/i],
							[
								[a, "UCBrowser"], p
							],
							[/(comodo_dragon)\/([\w\.]+)/i],
							[
								[a, /_/g, " "], p
							],
							[/(windowswechat qbcore)\/([\w\.]+)/i],
							[
								[a, "WeChat(Win) Desktop"], p
							],
							[/(micromessenger)\/([\w\.]+)/i],
							[
								[a, "WeChat"], p
							],
							[/(brave)\/([\w\.]+)/i],
							[
								[a, "Brave"], p
							],
							[/(whale)\/([\w\.]+)/i],
							[
								[a, "Whale"], p
							],
							[/(qqbrowserlite)\/([\w\.]+)/i],
							[a, p],
							[/(QQ)\/([\d\.]+)/i],
							[a, p],
							[/m?(qqbrowser)[\/\s]?([\w\.]+)/i],
							[a, p],
							[/(baiduboxapp)[\/\s]?([\w\.]+)/i],
							[a, p],
							[/(2345Explorer)[\/\s]?([\w\.]+)/i],
							[a, p],
							[/(MetaSr)[\/\s]?([\w\.]+)/i],
							[a],
							[/(LBBROWSER)/i],
							[a],
							[/xiaomi\/miuibrowser\/([\w\.]+)/i],
							[p, [a, "MIUI Browser"]],
							[/;fbav\/([\w\.]+);/i],
							[p, [a, "Facebook"]],
							[/FBAN\/FBIOS|FB_IAB\/FB4A/i],
							[
								[a, "Facebook"]
							],
							[/safari\s(line)\/([\w\.]+)/i,
								/android.+(line)\/([\w\.]+)\/iab/i
							],
							[a, p],
							[/headlesschrome(?:\/([\w\.]+)|\s)/i],
							[p, [a, "Chrome Headless"]],
							[/\swv\).+(chrome)\/([\w\.]+)/i],
							[
								[a, /(.+)/, "$1 WebView"], p
							],
							[/((?:oculus|samsung)browser)\/([\w\.]+)/i],
							[
								[a, /(.+(?:g|us))(.+)/, "$1 $2"], p
							],
							[/android.+version\/([\w\.]+)\s+(?:mobile\s?safari|safari)*/i],
							[p, [a, "Android Browser"]],
							[/(sailfishbrowser)\/([\w\.]+)/i],
							[
								[a, "Sailfish Browser"], p
							],
							[
							/(chrome|omniweb|arora|[tizenoka]{5}\s?browser)\/v?([\w\.]+)/i],
							[a, p],
							[/(dolfin)\/([\w\.]+)/i],
							[
								[a, "Dolphin"], p
							],
							[/(qihu|qhbrowser|qihoobrowser|360browser)/i],
							[
								[a, "360 Browser"]
							],
							[/((?:android.+)crmo|crios)\/([\w\.]+)/i],
							[
								[a, "Chrome"], p
							],
							[/(coast)\/([\w\.]+)/i],
							[
								[a, "Opera Coast"], p
							],
							[/fxios\/([\w\.-]+)/i],
							[p, [a, "Firefox"]],
							[/version\/([\w\.]+)\s.*mobile\/\w+\s(safari)/i],
							[p, [a, "Mobile Safari"]],
							[/version\/([\w\.]+)\s.*(mobile\s?safari|safari)/i],
							[p, a],
							[
								/webkit.+?(gsa)\/([\w\.]+)\s.*(mobile\s?safari|safari)(\/[\w\.]+)/i],
							[
								[a, "GSA"], p
							],
							[/webkit.+?(mobile\s?safari|safari)(\/[\w\.]+)/i],
							[a, [p, y.str, w.browser.oldsafari.version]],
							[/(webkit|khtml)\/([\w\.]+)/i],
							[a, p],
							[/(navigator|netscape)\/([\w\.-]+)/i],
							[
								[a, "Netscape"], p
							],
							[/(swiftfox)/i,
								/(icedragon|iceweasel|camino|chimera|fennec|maemo\sbrowser|minimo|conkeror)[\/\s]?([\w\.\+]+)/i,
								/(firefox|seamonkey|k-meleon|icecat|iceape|firebird|phoenix|palemoon|basilisk|waterfox)\/([\w\.-]+)$/i,
								/(firefox)\/([\w\.]+)\s[\w\s\-]+\/[\w\.]+$/i,
								/(mozilla)\/([\w\.]+)\s.+rv\:.+gecko\/\d+/i,
								/(polaris|lynx|dillo|icab|doris|amaya|w3m|netsurf|sleipnir)[\/\s]?([\w\.]+)/i,
								/(links)\s\(([\w\.]+)/i, /(gobrowser)\/?([\w\.]*)/i,
								/(ice\s?browser)\/v?([\w\._]+)/i, /(mosaic)[\/\s]([\w\.]+)/i
							],
							[a, p]
						],
						cpu: [
							[/(?:(amd|x(?:(?:86|64)[_-])?|wow|win)64)[;\)]/i],
							[
								[l, "amd64"]
							],
							[/(ia32(?=;))/i],
							[
								[l, g.lowerize]
							],
							[/((?:i[346]|x)86)[;\)]/i],
							[
								[l, "ia32"]
							],
							[/windows\s(ce|mobile);\sppc;/i],
							[
								[l, "arm"]
							],
							[/((?:ppc|powerpc)(?:64)?)(?:\smac|;|\))/i],
							[
								[l, /ower/, "", g.lowerize]
							],
							[/(sun4\w)[;\)]/i],
							[
								[l, "sparc"]
							],
							[
								/((?:avr32|ia64(?=;))|68k(?=\))|arm(?:64|(?=v\d+[;l]))|(?=atmel\s)avr|(?:irix|mips|sparc)(?:64)?(?=;)|pa-risc)/i],
							[
								[l, g.lowerize]
							]
						],
						device: [
							[/\((ipad|playbook);[\w\s\),;-]+(rim|apple)/i],
							[s, d, [c, h]],
							[/applecoremedia\/[\w\.]+ \((ipad)/],
							[s, [d, "Apple"],
								[c, h]
							],
							[/(apple\s{0,1}tv)/i],
							[
								[s, "Apple TV"],
								[d, "Apple"],
								[c, m]
							],
							[/(archos)\s(gamepad2?)/i, /(hp).+(touchpad)/i,
								/(hp).+(tablet)/i, /(kindle)\/([\w\.]+)/i,
								/\s(nook)[\w\s]+build\/(\w+)/i,
								/(dell)\s(strea[kpr\s\d]*[\dko])/i
							],
							[d, s, [c, h]],
							[/(kf[A-z]+)(\sbuild\/|\)).+silk\//i],
							[s, [d, "Amazon"],
								[c, h]
							],
							[/(sd|kf)[0349hijorstuw]+(\sbuild\/|\)).+silk\//i],
							[
								[s, y.str, w.device.amazon.model],
								[d, "Amazon"],
								[c, f]
							],
							[/android.+aft([bms])\sbuild/i],
							[s, [d, "Amazon"],
								[c, m]
							],
							[/\((ip[honed|\s\w*]+);.+(apple)/i],
							[s, d, [c, f]],
							[/\((ip[honed|\s\w*]+);/i],
							[s, [d, "Apple"],
								[c, f]
							],
							[/(blackberry)[\s-]?(\w+)/i,
								/(blackberry|benq|palm(?=\-)|sonyericsson|acer|asus|dell|meizu|motorola|polytron)[\s_-]?([\w-]*)/i,
								/(hp)\s([\w\s]+\w)/i, /(asus)-?(\w+)/i
							],
							[d, s, [c, f]],
							[/\(bb10;\s(\w+)/i],
							[s, [d, "BlackBerry"],
								[c, f]
							],
							[
								/android.+(transfo[prime\s]{4,10}\s\w+|eeepc|slider\s\w+|nexus 7|padfone|p00c)/i],
							[s, [d, "Asus"],
								[c, h]
							],
							[/(sony)\s(tablet\s[ps])\sbuild\//i,
								/(sony)?(?:sgp.+)\sbuild\//i
							],
							[
								[d, "Sony"],
								[s, "Xperia Tablet"],
								[c, h]
							],
							[
								/android.+\s([c-g]\d{4}|so[-l]\w+)(?=\sbuild\/|\).+chrome\/(?![1-6]{0,1}\d\.))/i],
							[s, [d, "Sony"],
								[c, f]
							],
							[/\s(ouya)\s/i, /(nintendo)\s([wids3u]+)/i],
							[d, s, [c, u]],
							[/android.+;\s(shield)\sbuild/i],
							[s, [d, "Nvidia"],
								[c, u]
							],
							[/(playstation\s[34portablevi]+)/i],
							[s, [d, "Sony"],
								[c, u]
							],
							[/(sprint\s(\w+))/i],
							[
								[d, y.str, w.device.sprint.vendor],
								[s, y.str, w.device.sprint.model],
								[c, f]
							],
							[/(htc)[;_\s-]{1,2}([\w\s]+(?=\)|\sbuild)|\w+)/i,
								/(zte)-(\w*)/i,
								/(alcatel|geeksphone|nexian|panasonic|(?=;\s)sony)[_\s-]?([\w-]*)/i
							],
							[d, [s, /_/g, " "],
								[c, f]
							],
							[/(nexus\s9)/i],
							[s, [d, "HTC"],
								[c, h]
							],
							[/d\/huawei([\w\s-]+)[;\)]/i,
								/android.+\s(nexus\s6p|vog-[at]?l\d\d|ane-[at]?l[x\d]\d|eml-a?l\d\da?|lya-[at]?l\d[\dc]|clt-a?l\d\di?)/i
							],
							[s, [d, "Huawei"],
								[c, f]
							],
							[/android.+(bah2?-a?[lw]\d{2})/i],
							[s, [d, "Huawei"],
								[c, h]
							],
							[/(microsoft);\s(lumia[\s\w]+)/i],
							[d, s, [c, f]],
							[/[\s\(;](xbox(?:\sone)?)[\s\);]/i],
							[s, [d, "Microsoft"],
								[c, u]
							],
							[/(kin\.[onetw]{3})/i],
							[
								[s, /\./g, " "],
								[d, "Microsoft"],
								[c, f]
							],
							[/\s(milestone|droid(?:[2-4x]|\s(?:bionic|x2|pro|razr))?:?(\s4g)?)[\w\s]+build\//i,
								/mot[\s-]?(\w*)/i, /(XT\d{3,4}) build\//i, /(nexus\s6)/i
							],
							[s, [d, "Motorola"],
								[c, f]
							],
							[/android.+\s(mz60\d|xoom[\s2]{0,2})\sbuild\//i],
							[s, [d, "Motorola"],
								[c, h]
							],
							[/hbbtv\/\d+\.\d+\.\d+\s+\([\w\s]*;\s*(\w[^;]*);([^;]*)/i],
							[
								[d, g.trim],
								[s, g.trim],
								[c, m]
							],
							[/hbbtv.+maple;(\d+)/i],
							[
								[s, /^/, "SmartTV"],
								[d, "Samsung"],
								[c, m]
							],
							[/\(dtv[\);].+(aquos)/i],
							[s, [d, "Sharp"],
								[c, m]
							],
							[/android.+((sch-i[89]0\d|shw-m380s|SM-P605|SM-P610|gt-p\d{4}|gt-n\d+|sgh-t8[56]9|nexus 10))/i,
								/((SM-T\w+))/i
							],
							[
								[d, "Samsung"], s, [c, h]
							],
							[/smart-tv.+(samsung)/i],
							[d, [c, m], s],
							[/((s[cgp]h-\w+|gt-\w+|galaxy\snexus|sm-\w[\w\d]+))/i,
								/(sam[sung]*)[\s-]*(\w+-?[\w-]*)/i, /sec-((sgh\w+))/i
							],
							[
								[d, "Samsung"], s, [c, f]
							],
							[/sie-(\w*)/i],
							[s, [d, "Siemens"],
								[c, f]
							],
							[/(maemo|nokia).*(n900|lumia\s\d+)/i,
							/(nokia)[\s_-]?([\w-]*)/i],
							[
								[d, "Nokia"], s, [c, f]
							],
							[/android[x\d\.\s;]+\s([ab][1-7]\-?[0178a]\d\d?)/i],
							[s, [d, "Acer"],
								[c, h]
							],
							[/android.+([vl]k\-?\d{3})\s+build/i],
							[s, [d, "LG"],
								[c, h]
							],
							[/android\s3\.[\s\w;-]{10}(lg?)-([06cv9]{3,4})/i],
							[
								[d, "LG"], s, [c, h]
							],
							[/linux;\snetcast.+smarttv/i, /lg\snetcast\.tv-201\d/i],
							[
								[d, "LG"], s, [c, m]
							],
							[/(nexus\s[45])/i, /lg[e;\s\/-]+(\w*)/i,
								/android.+lg(\-?[\d\w]+)\s+build/i
							],
							[s, [d, "LG"],
								[c, f]
							],
							[/(lenovo)\s?(s(?:5000|6000)(?:[\w-]+)|tab(?:[\s\w]+))/i],
							[d, s, [c, h]],
							[/android.+(ideatab[a-z0-9\-\s]+)/i],
							[s, [d, "Lenovo"],
								[c, h]
							],
							[/(lenovo)[_\s-]?([\w-]+)/i],
							[d, s, [c, f]],
							[/linux;.+((jolla));/i],
							[d, s, [c, f]],
							[/((pebble))app\/[\d\.]+\s/i],
							[d, s, [c, v]],
							[/android.+;\s(oppo)\s?([\w\s]+)\sbuild/i],
							[d, s, [c, f]],
							[/crkey/i],
							[
								[s, "Chromecast"],
								[d, "Google"],
								[c, m]
							],
							[/android.+;\s(glass)\s\d/i],
							[s, [d, "Google"],
								[c, v]
							],
							[/android.+;\s(pixel c)[\s)]/i],
							[s, [d, "Google"],
								[c, h]
							],
							[/android.+;\s(pixel( [2-9]a?)?( xl)?)[\s)]/i],
							[s, [d, "Google"],
								[c, f]
							],
							[/android.+;\s(\w+)\s+build\/hm\1/i,
								/android.+(hm[\s\-_]?note?[\s_]?(?:\d\w)?)\sbuild/i,
								/android.+(redmi[\s\-_]?(?:note|k)?(?:[\s_]?[\w\s]+))(?:\sbuild|\))/i,
								/android.+(mi[\s\-_]?(?:a\d|one|one[\s_]plus|note lte)?[\s_]?(?:\d?\w?)[\s_]?(?:plus)?)\sbuild/i
							],
							[
								[s, /_/g, " "],
								[d, "Xiaomi"],
								[c, f]
							],
							[
							/android.+(mi[\s\-_]?(?:pad)(?:[\s_]?[\w\s]+))(?:\sbuild|\))/i],
							[
								[s, /_/g, " "],
								[d, "Xiaomi"],
								[c, h]
							],
							[/android.+;\s(m[1-5]\snote)\sbuild/i],
							[s, [d, "Meizu"],
								[c, f]
							],
							[/(mz)-([\w-]{2,})/i],
							[
								[d, "Meizu"], s, [c, f]
							],
							[/android.+a000(1)\s+build/i,
								/android.+oneplus\s(a\d{4})[\s)]/i],
							[s, [d, "OnePlus"],
								[c, f]
							],
							[/android.+[;\/]\s*(RCT[\d\w]+)\s+build/i],
							[s, [d, "RCA"],
								[c, h]
							],
							[/android.+[;\/\s](Venue[\d\s]{2,7})\s+build/i],
							[s, [d, "Dell"],
								[c, h]
							],
							[/android.+[;\/]\s*(Q[T|M][\d\w]+)\s+build/i],
							[s, [d, "Verizon"],
								[c, h]
							],
							[
								/android.+[;\/]\s+(Barnes[&\s]+Noble\s+|BN[RT])(V?.*)\s+build/i],
							[
								[d, "Barnes & Noble"], s, [c, h]
							],
							[/android.+[;\/]\s+(TM\d{3}.*\b)\s+build/i],
							[s, [d, "NuVision"],
								[c, h]
							],
							[/android.+;\s(k88)\sbuild/i],
							[s, [d, "ZTE"],
								[c, h]
							],
							[/android.+[;\/]\s*(gen\d{3})\s+build.*49h/i],
							[s, [d, "Swiss"],
								[c, f]
							],
							[/android.+[;\/]\s*(zur\d{3})\s+build/i],
							[s, [d, "Swiss"],
								[c, h]
							],
							[/android.+[;\/]\s*((Zeki)?TB.*\b)\s+build/i],
							[s, [d, "Zeki"],
								[c, h]
							],
							[/(android).+[;\/]\s+([YR]\d{2})\s+build/i,
								/android.+[;\/]\s+(Dragon[\-\s]+Touch\s+|DT)(\w{5})\sbuild/i
							],
							[
								[d, "Dragon Touch"], s, [c, h]
							],
							[/android.+[;\/]\s*(NS-?\w{0,9})\sbuild/i],
							[s, [d, "Insignia"],
								[c, h]
							],
							[/android.+[;\/]\s*((NX|Next)-?\w{0,9})\s+build/i],
							[s, [d, "NextBook"],
								[c, h]
							],
							[
								/android.+[;\/]\s*(Xtreme\_)?(V(1[045]|2[015]|30|40|60|7[05]|90))\s+build/i],
							[
								[d, "Voice"], s, [c, f]
							],
							[/android.+[;\/]\s*(LVTEL\-)?(V1[12])\s+build/i],
							[
								[d, "LvTel"], s, [c, f]
							],
							[/android.+;\s(PH-1)\s/i],
							[s, [d, "Essential"],
								[c, f]
							],
							[/android.+[;\/]\s*(V(100MD|700NA|7011|917G).*\b)\s+build/i],
							[s, [d, "Envizen"],
								[c, h]
							],
							[/android.+[;\/]\s*(Le[\s\-]+Pan)[\s\-]+(\w{1,9})\s+build/i],
							[d, s, [c, h]],
							[/android.+[;\/]\s*(Trio[\s\w\-\.]+)\s+build/i],
							[s, [d, "MachSpeed"],
								[c, h]
							],
							[/android.+[;\/]\s*(Trinity)[\-\s]*(T\d{3})\s+build/i],
							[d, s, [c, h]],
							[/android.+[;\/]\s*TU_(1491)\s+build/i],
							[s, [d, "Rotor"],
								[c, h]
							],
							[/android.+(Gigaset)[\s\-]+(Q\w{1,9})\s+build/i],
							[d, s, [c, h]],
							[
								/android .+?; ([^;]+?)(?: build|\) applewebkit).+? mobile safari/i],
							[s, [c, f]],
							[
								/android .+?;\s([^;]+?)(?: build|\) applewebkit).+?(?! mobile) safari/i],
							[s, [c, h]],
							[/\s(tablet|tab)[;\/]/i, /\s(mobile)(?:[;\/]|\ssafari)/i],
							[
								[c, g.lowerize], d, s
							],
							[/[\s\/\(](smart-?tv)[;\)]/i],
							[
								[c, m]
							],
							[/(android[\w\.\s\-]{0,9});.+build/i],
							[s, [d, "Generic"]]
						],
						engine: [
							[/windows.+\sedge\/([\w\.]+)/i],
							[p, [a, "EdgeHTML"]],
							[/webkit\/537\.36.+chrome\/(?!27)([\w\.]+)/i],
							[p, [a, "Blink"]],
							[/(presto)\/([\w\.]+)/i,
								/(webkit|trident|netfront|netsurf|amaya|lynx|w3m|goanna)\/([\w\.]+)/i,
								/(khtml|tasman|links)[\/\s]\(?([\w\.]+)/i,
								/(icab)[\/\s]([23]\.[\d\.]+)/i
							],
							[a, p],
							[/rv\:([\w\.]{1,9}).+(gecko)/i],
							[p, a]
						],
						os: [
							[/microsoft\s(windows)\s(vista|xp)/i],
							[a, p],
							[/(windows)\snt\s6\.2;\s(arm)/i,
								/(windows\sphone(?:\sos)*)[\s\/]?([\d\.\s\w]*)/i,
								/(windows\smobile|windows)[\s\/]?([ntce\d\.\s]+\w)/i
							],
							[a, [p, y.str, w.os.windows.version]],
							[/(win(?=3|9|n)|win\s9x\s)([nt\d\.]+)/i],
							[
								[a, "Windows"],
								[p, y.str, w.os.windows.version]
							],
							[/\((bb)(10);/i],
							[
								[a, "BlackBerry"], p
							],
							[/(blackberry)\w*\/?([\w\.]*)/i,
								/(tizen|kaios)[\/\s]([\w\.]+)/i,
								/(android|webos|palm\sos|qnx|bada|rim\stablet\sos|meego|sailfish|contiki)[\/\s-]?([\w\.]*)/i
							],
							[a, p],
							[/(symbian\s?os|symbos|s60(?=;))[\/\s-]?([\w\.]*)/i],
							[
								[a, "Symbian"], p
							],
							[/\((series40);/i],
							[a],
							[/mozilla.+\(mobile;.+gecko.+firefox/i],
							[
								[a, "Firefox OS"], p
							],
							[/crkey\/([\d\.]+)/i],
							[p, [a, "Chromecast"]],
							[/(nintendo|playstation)\s([wids34portablevu]+)/i,
								/(mint)[\/\s\(]?(\w*)/i, /(mageia|vectorlinux)[;\s]/i,
								/(joli|[kxln]?ubuntu|debian|suse|opensuse|gentoo|(?=\s)arch|slackware|fedora|mandriva|centos|pclinuxos|redhat|zenwalk|linpus)[\/\s-]?(?!chrom)([\w\.-]*)/i,
								/(hurd|linux)\s?([\w\.]*)/i, /(gnu)\s?([\w\.]*)/i
							],
							[a, p],
							[/(cros)\s[\w]+\s([\w\.]+\w)/i],
							[
								[a, "Chromium OS"], p
							],
							[/(sunos)\s?([\w\.\d]*)/i],
							[
								[a, "Solaris"], p
							],
							[/\s([frentopc-]{0,4}bsd|dragonfly)\s?([\w\.]*)/i],
							[a, p],
							[/(haiku)\s(\w+)/i],
							[a, p],
							[/cfnetwork\/.+darwin/i,
								/ip[honead]{2,4}(?:.*os\s([\w]+)\slike\smac|;\sopera)/i
							],
							[
								[p, /_/g, "."],
								[a, "iOS"]
							],
							[/(mac\sos\sx)\s?([\w\s\.]*)/i,
								/(macintosh|mac(?=_powerpc)\s)/i],
							[
								[a, "Mac OS"],
								[p, /_/g, "."]
							],
							[/((?:open)?solaris)[\/\s-]?([\w\.]*)/i,
								/(aix)\s((\d)(?=\.|\)|\s)[\w\.])*/i,
								/(plan\s9|minix|beos|os\/2|amigaos|morphos|risc\sos|openvms|fuchsia)/i,
								/(unix)\s?([\w\.]*)/i
							],
							[a, p]
						]
					},
					C = function(e, t) {
						if ("object" == typeof e && (t = e, e = n), !(this instanceof C))
						return new C(e, t).getResult();
						var i = e || (r && r.navigator && r.navigator.userAgent ? r.navigator
								.userAgent : ""),
							o = t ? g.extend(T, t) : T;
						return this.getBrowser = function() {
							var e = {
								name: n,
								version: n
							};
							return y.rgx.call(e, i, o.browser), e.major = g.major(e
								.version), e
						}, this.getCPU = function() {
							var e = {
								architecture: n
							};
							return y.rgx.call(e, i, o.cpu), e
						}, this.getDevice = function() {
							var e = {
								vendor: n,
								model: n,
								type: n
							};
							return y.rgx.call(e, i, o.device), e
						}, this.getEngine = function() {
							var e = {
								name: n,
								version: n
							};
							return y.rgx.call(e, i, o.engine), e
						}, this.getOS = function() {
							var e = {
								name: n,
								version: n
							};
							return y.rgx.call(e, i, o.os), e
						}, this.getResult = function() {
							return {
								ua: this.getUA(),
								browser: this.getBrowser(),
								engine: this.getEngine(),
								os: this.getOS(),
								device: this.getDevice(),
								cpu: this.getCPU()
							}
						}, this.getUA = function() {
							return i
						}, this.setUA = function(e) {
							return i = e, this
						}, this
					};
				C.VERSION = "0.7.23", C.BROWSER = {
					NAME: a,
					MAJOR: "major",
					VERSION: p
				}, C.CPU = {
					ARCHITECTURE: l
				}, C.DEVICE = {
					MODEL: s,
					VENDOR: d,
					TYPE: c,
					CONSOLE: u,
					MOBILE: f,
					SMARTTV: m,
					TABLET: h,
					WEARABLE: v,
					EMBEDDED: "embedded"
				}, C.ENGINE = {
					NAME: a,
					VERSION: p
				}, C.OS = {
					NAME: a,
					VERSION: p
				}, e.exports && (t = e.exports = C), t.UAParser = C;
				var S = r && (r.jQuery || r.Zepto);
				if (S && !S.ua) {
					var b = new C;
					S.ua = b.getResult(), S.ua.get = function() {
						return b.getUA()
					}, S.ua.set = function(e) {
						b.setUA(e);
						var t = b.getResult();
						for (var r in t) S.ua[r] = t[r]
					}
				}
			}("object" == typeof window ? window : c)
		})).UAParser)).getResult(),
		l = {
			osName: p.os.name || "",
			osVersion: p.os.version || "",
			browserName: p.browser.name || "",
			browserVersion: p.browser.version || ""
		};

	function u(e, t) {
		return i(this, void 0, void 0, (function() {
			var r, n, i, s, a, c;
			return o(this, (function(o) {
				switch (o.label) {
					case 0:
						r = {
							method: "POST",
							headers: {
								"Content-Type": "application/json"
							},
							body: JSON.stringify(t)
						}, "AbortController" in window && (n = new AbortController,
							setTimeout((function() {
								return n.abort()
							}), b), r.signal = n.signal), o.label = 1;
					case 1:
						return o.trys.push([1, 3, , 4]), [4, fetch(e, r)];
					case 2:
						return i = o.sent(), [3, 4];
					case 3:
						throw s = o.sent(), c = void 0, c = "AbortError" === s.name ?
							"pullStreamRequest, error: " + b / 1e3 + "s timeout" :
							"pullStreamRequest, error: " + s.message, _(c), new T(c);
					case 4:
						if (200 !== i.status) throw c =
							"pullStreamRequest, statusCode error: statusCode: " + i
							.status + ", statusText: " + i.statusText, _(c), new T(
								c);
						o.label = 5;
					case 5:
						return o.trys.push([5, 7, , 8]), [4, i.json()];
					case 6:
						return a = o.sent(), [3, 8];
					case 7:
						throw o.sent(), c = "parse response as json error: " + i.text(),
							O(c), new T(c);
					case 8:
						if ([400, 500].includes(a.code)) throw O(a.msg), new T(a.msg);
						if (403 === a.code) throw x(a.msg), new T(a.msg);
						if (404 === a.code) throw D(a.msg), new T(a.msg);
						if (![0, 200].includes(a.code)) throw new T(
							"unexpected code: " + a.code + ", msg: " + a.msg);
						return [2, a]
				}
			}))
		}))
	}

	function f() {
		var e = new Date;

		function t(e) {
			var t = e.toString();
			return t.length < 2 ? "0" + t : t
		}
		return "[" + t(e.getHours()) + ":" + t(e.getMinutes()) + ":" + t(e.getSeconds()) + "." + e
			.getMilliseconds() + "]"
	}
	var h = new(function() {
		function e(e) {
			this.level = e
		}
		return e.prototype.setLevel = function(e) {
			this.level = e
		}, e.prototype.log = function(e) {
			if ("log" === this.level) {
				var t = f(),
					r = t + " %cLOG-QNRTPLAYER";
				console.info(r, "color: #66ccff; font-weight: bold;", e);
				var n = {
					time: t,
					level: "log",
					msg: e,
					id: v(8)
				};
				k(n)
			}
		}, e.prototype.debug = function(e) {
			if ("log" === this.level || "debug" === this.level) {
				var t = f(),
					r = t + " %cDEBUG-QNRTPLAYER";
				console.info(r, "color: #A28148; font-weight: bold;", e);
				var n = {
					time: t,
					level: "debug",
					msg: e,
					id: v(8)
				};
				k(n)
			}
		}, e.prototype.warning = function(e) {
			if ("disable" !== this.level) {
				var t = f(),
					r = t + " %cWARNING-QNRTPLAYER";
				console.warn(r, "color: #E44F44; font-weight: bold;", e);
				var n = {
					time: t,
					level: "warning",
					msg: e,
					id: v(8)
				};
				k(n)
			}
		}, e
	}())("log");

	function m(e) {
		return ("0" + e.toString(16)).substr(-2)
	}

	function v(e) {
		void 0 === e && (e = 5);
		var t = new Uint8Array((e || 40) / 2);
		return window.crypto.getRandomValues(t), Array.from(t, m).join("")
	}

	function g(e, t) {
		void 0 === t && (t = !1);
		try {
			return t ? JSON.stringify(e, null, 2) : JSON.stringify(e)
		} catch (e) {
			return h.warning("json stringify error: " + g(e)), "stringify error"
		}
	}

	function y(e, t) {
		var r = Math.pow(10, t);
		return Math.round(e * r) / r
	}
	var w, T = function(e) {
			function t(t) {
				var r = e.call(this, t) || this;
				return r.msg = t, h.warning("SDK Error: " + t), r
			}
			return r(t, e), t
		}(Error),
		C = {
			className: "qn-rtplayer-media",
			width: "100%",
			height: "100%",
			objectFit: "contain",
			volumn: .6,
			controls: !1,
			playsinline: !0
		},
		S = {
			audioBitrate: 0,
			videoBitrate: 0,
			frameWidth: 0,
			frameHeight: 0,
			frameRate: 0
		};
	! function(e) {
		e[e.STATE_IDLE = 0] = "STATE_IDLE", e[e.STATE_INIT = 1] = "STATE_INIT", e[e.STATE_READY = 2] =
			"STATE_READY", e[e.STATE_PLAYING = 3] = "STATE_PLAYING", e[e.STATE_STOP = 4] = "STATE_STOP", e[e
				.STATE_ERROR = 5] = "STATE_ERROR"
	}(w || (w = {}));
	var b = 8e3,
		R = "1.0.3",
		E = d((function(e) {
			! function(t) {
				function r() {}
				var n = r.prototype,
					i = t.EventEmitter;

				function o(e, t) {
					for (var r = e.length; r--;)
						if (e[r].listener === t) return r;
					return -1
				}

				function s(e) {
					return function() {
						return this[e].apply(this, arguments)
					}
				}

				function a(e) {
					return "function" == typeof e || e instanceof RegExp || !(!e || "object" !=
						typeof e) && a(e.listener)
				}
				n.getListeners = function(e) {
					var t, r, n = this._getEvents();
					if (e instanceof RegExp)
						for (r in t = {}, n) n.hasOwnProperty(r) && e.test(r) && (t[r] = n[r]);
					else t = n[e] || (n[e] = []);
					return t
				}, n.flattenListeners = function(e) {
					var t, r = [];
					for (t = 0; t < e.length; t += 1) r.push(e[t].listener);
					return r
				}, n.getListenersAsObject = function(e) {
					var t, r = this.getListeners(e);
					return r instanceof Array && ((t = {})[e] = r), t || r
				}, n.addListener = function(e, t) {
					if (!a(t)) throw new TypeError("listener must be a function");
					var r, n = this.getListenersAsObject(e),
						i = "object" == typeof t;
					for (r in n) n.hasOwnProperty(r) && -1 === o(n[r], t) && n[r].push(i ? t : {
						listener: t,
						once: !1
					});
					return this
				}, n.on = s("addListener"), n.addOnceListener = function(e, t) {
					return this.addListener(e, {
						listener: t,
						once: !0
					})
				}, n.once = s("addOnceListener"), n.defineEvent = function(e) {
					return this.getListeners(e), this
				}, n.defineEvents = function(e) {
					for (var t = 0; t < e.length; t += 1) this.defineEvent(e[t]);
					return this
				}, n.removeListener = function(e, t) {
					var r, n, i = this.getListenersAsObject(e);
					for (n in i) i.hasOwnProperty(n) && -1 !== (r = o(i[n], t)) && i[n].splice(r,
					1);
					return this
				}, n.off = s("removeListener"), n.addListeners = function(e, t) {
					return this.manipulateListeners(!1, e, t)
				}, n.removeListeners = function(e, t) {
					return this.manipulateListeners(!0, e, t)
				}, n.manipulateListeners = function(e, t, r) {
					var n, i, o = e ? this.removeListener : this.addListener,
						s = e ? this.removeListeners : this.addListeners;
					if ("object" != typeof t || t instanceof RegExp)
						for (n = r.length; n--;) o.call(this, t, r[n]);
					else
						for (n in t) t.hasOwnProperty(n) && (i = t[n]) && ("function" == typeof i ?
							o.call(this, n, i) : s.call(this, n, i));
					return this
				}, n.removeEvent = function(e) {
					var t, r = typeof e,
						n = this._getEvents();
					if ("string" === r) delete n[e];
					else if (e instanceof RegExp)
						for (t in n) n.hasOwnProperty(t) && e.test(t) && delete n[t];
					else delete this._events;
					return this
				}, n.removeAllListeners = s("removeEvent"), n.emitEvent = function(e, t) {
					var r, n, i, o, s = this.getListenersAsObject(e);
					for (o in s)
						if (s.hasOwnProperty(o))
							for (r = s[o].slice(0), i = 0; i < r.length; i++) !0 === (n = r[i])
								.once && this.removeListener(e, n.listener), n.listener.apply(this,
									t || []) === this._getOnceReturnValue() && this.removeListener(
									e, n.listener);
					return this
				}, n.trigger = s("emitEvent"), n.emit = function(e) {
					var t = Array.prototype.slice.call(arguments, 1);
					return this.emitEvent(e, t)
				}, n.setOnceReturnValue = function(e) {
					return this._onceReturnValue = e, this
				}, n._getOnceReturnValue = function() {
					return !this.hasOwnProperty("_onceReturnValue") || this._onceReturnValue
				}, n._getEvents = function() {
					return this._events || (this._events = {})
				}, r.noConflict = function() {
					return t.EventEmitter = i, r
				}, e.exports ? e.exports = r : t.EventEmitter = r
			}("undefined" != typeof window ? window : c || {})
		})),
		P = new E,
		k = function(e) {
			P.emit("log", e)
		},
		_ = function(e) {
			var t = {
				code: 20001,
				errorType: "networkError",
				msg: e
			};
			P.emit("error", t)
		},
		x = function(e) {
			var t = {
				code: 20002,
				errorType: "authFailed",
				msg: e
			};
			P.emit("error", t)
		},
		D = function(e) {
			var t = {
				code: 20003,
				errorType: "playStreamNotExist",
				msg: e
			};
			P.emit("error", t)
		},
		O = function(e) {
			var t = {
				code: 20004,
				errorType: "playRequestFailed",
				msg: e
			};
			P.emit("error", t)
		},
		I = function(e) {
			var t = {
				code: 20005,
				errorType: "descriptionError",
				msg: e
			};
			P.emit("error", t)
		},
		M = function(e) {
			var t = {
				code: 30001,
				errorType: "rtcNotSupport",
				msg: e
			};
			P.emit("error", t)
		};
	let L = !0,
		A = !0;

	function j(e, t, r) {
		const n = e.match(t);
		return n && n.length >= r && parseInt(n[r], 10)
	}

	function N(e, t, r) {
		if (!e.RTCPeerConnection) return;
		const n = e.RTCPeerConnection.prototype,
			i = n.addEventListener;
		n.addEventListener = function(e, n) {
			if (e !== t) return i.apply(this, arguments);
			const o = e => {
				const t = r(e);
				t && (n.handleEvent ? n.handleEvent(t) : n(t))
			};
			return this._eventMap = this._eventMap || {}, this._eventMap[t] || (this._eventMap[t] =
				new Map), this._eventMap[t].set(n, o), i.apply(this, [e, o])
		};
		const o = n.removeEventListener;
		n.removeEventListener = function(e, r) {
			if (e !== t || !this._eventMap || !this._eventMap[t]) return o.apply(this, arguments);
			if (!this._eventMap[t].has(r)) return o.apply(this, arguments);
			const n = this._eventMap[t].get(r);
			return this._eventMap[t].delete(r), 0 === this._eventMap[t].size && delete this._eventMap[t],
				0 === Object.keys(this._eventMap).length && delete this._eventMap, o.apply(this, [e, n])
		}, Object.defineProperty(n, "on" + t, {
			get() {
				return this["_on" + t]
			},
			set(e) {
				this["_on" + t] && (this.removeEventListener(t, this["_on" + t]), delete this[
					"_on" + t]), e && this.addEventListener(t, this["_on" + t] = e)
			},
			enumerable: !0,
			configurable: !0
		})
	}

	function z(e) {
		return "boolean" != typeof e ? new Error("Argument type: " + typeof e + ". Please use a boolean.") : (
			L = e, e ? "adapter.js logging disabled" : "adapter.js logging enabled")
	}

	function G(e) {
		return "boolean" != typeof e ? new Error("Argument type: " + typeof e + ". Please use a boolean.") : (
			A = !e, "adapter.js deprecation warnings " + (e ? "disabled" : "enabled"))
	}

	function F() {
		if ("object" == typeof window) {
			if (L) return;
			"undefined" != typeof console && "function" == typeof console.log && console.log.apply(console,
				arguments)
		}
	}

	function U(e, t) {
		A && console.warn(e + " is deprecated, please use " + t + " instead.")
	}

	function V(e) {
		const t = {
			browser: null,
			version: null
		};
		if (void 0 === e || !e.navigator) return t.browser = "Not a browser.", t;
		const {
			navigator: r
		} = e;
		if (r.mozGetUserMedia) t.browser = "firefox", t.version = j(r.userAgent, /Firefox\/(\d+)\./, 1);
		else if (r.webkitGetUserMedia || !1 === e.isSecureContext && e.webkitRTCPeerConnection && !e
			.RTCIceGatherer) t.browser = "chrome", t.version = j(r.userAgent, /Chrom(e|ium)\/(\d+)\./, 2);
		else if (r.mediaDevices && r.userAgent.match(/Edge\/(\d+).(\d+)$/)) t.browser = "edge", t.version = j(r
			.userAgent, /Edge\/(\d+).(\d+)$/, 2);
		else {
			if (!e.RTCPeerConnection || !r.userAgent.match(/AppleWebKit\/(\d+)\./)) return t.browser =
				"Not a supported browser.", t;
			t.browser = "safari", t.version = j(r.userAgent, /AppleWebKit\/(\d+)\./, 1), t.supportsUnifiedPlan =
				e.RTCRtpTransceiver && "currentDirection" in e.RTCRtpTransceiver.prototype
		}
		return t
	}

	function B(e) {
		return "[object Object]" === Object.prototype.toString.call(e)
	}

	function J(e) {
		return B(e) ? Object.keys(e).reduce((function(t, r) {
			const n = B(e[r]),
				i = n ? J(e[r]) : e[r],
				o = n && !Object.keys(i).length;
			return void 0 === i || o ? t : Object.assign(t, {
				[r]: i
			})
		}), {}) : e
	}

	function q(e, t, r) {
		t && !r.has(t.id) && (r.set(t.id, t), Object.keys(t).forEach((n => {
			n.endsWith("Id") ? q(e, e.get(t[n]), r) : n.endsWith("Ids") && t[n].forEach((t => {
				q(e, e.get(t), r)
			}))
		})))
	}

	function W(e, t, r) {
		const n = r ? "outbound-rtp" : "inbound-rtp",
			i = new Map;
		if (null === t) return i;
		const o = [];
		return e.forEach((e => {
			"track" === e.type && e.trackIdentifier === t.id && o.push(e)
		})), o.forEach((t => {
			e.forEach((r => {
				r.type === n && r.trackId === t.id && q(e, r, i)
			}))
		})), i
	}
	const H = F;

	function Y(e) {
		const t = e && e.navigator;
		if (!t.mediaDevices) return;
		const r = V(e),
			n = function(e) {
				if ("object" != typeof e || e.mandatory || e.optional) return e;
				const t = {};
				return Object.keys(e).forEach((r => {
					if ("require" === r || "advanced" === r || "mediaSource" === r) return;
					const n = "object" == typeof e[r] ? e[r] : {
						ideal: e[r]
					};
					void 0 !== n.exact && "number" == typeof n.exact && (n.min = n.max = n.exact);
					const i = function(e, t) {
						return e ? e + t.charAt(0).toUpperCase() + t.slice(1) : "deviceId" ===
							t ? "sourceId" : t
					};
					if (void 0 !== n.ideal) {
						t.optional = t.optional || [];
						let e = {};
						"number" == typeof n.ideal ? (e[i("min", r)] = n.ideal, t.optional.push(e),
							e = {}, e[i("max", r)] = n.ideal, t.optional.push(e)) : (e[i("",
							r)] = n.ideal, t.optional.push(e))
					}
					void 0 !== n.exact && "number" != typeof n.exact ? (t.mandatory = t.mandatory ||
					{}, t.mandatory[i("", r)] = n.exact) : ["min", "max"].forEach((e => {
						void 0 !== n[e] && (t.mandatory = t.mandatory || {}, t
							.mandatory[i(e, r)] = n[e])
					}))
				})), e.advanced && (t.optional = (t.optional || []).concat(e.advanced)), t
			},
			i = function(e, i) {
				if (r.version >= 61) return i(e);
				if ((e = JSON.parse(JSON.stringify(e))) && "object" == typeof e.audio) {
					const t = function(e, t, r) {
						t in e && !(r in e) && (e[r] = e[t], delete e[t])
					};
					t((e = JSON.parse(JSON.stringify(e))).audio, "autoGainControl", "googAutoGainControl"), t(e
						.audio, "noiseSuppression", "googNoiseSuppression"), e.audio = n(e.audio)
				}
				if (e && "object" == typeof e.video) {
					let o = e.video.facingMode;
					o = o && ("object" == typeof o ? o : {
						ideal: o
					});
					const s = r.version < 66;
					if (o && ("user" === o.exact || "environment" === o.exact || "user" === o.ideal ||
							"environment" === o.ideal) && (!t.mediaDevices.getSupportedConstraints || !t
							.mediaDevices.getSupportedConstraints().facingMode || s)) {
						let r;
						if (delete e.video.facingMode, "environment" === o.exact || "environment" === o.ideal ?
							r = ["back", "rear"] : "user" !== o.exact && "user" !== o.ideal || (r = ["front"]),
							r) return t.mediaDevices.enumerateDevices().then((t => {
							let s = (t = t.filter((e => "videoinput" === e.kind))).find((e => r
								.some((t => e.label.toLowerCase().includes(t)))));
							return !s && t.length && r.includes("back") && (s = t[t.length -
								1]), s && (e.video.deviceId = o.exact ? {
									exact: s.deviceId
								} : {
									ideal: s.deviceId
								}), e.video = n(e.video), H("chrome: " + JSON.stringify(e)), i(
									e)
						}))
					}
					e.video = n(e.video)
				}
				return H("chrome: " + JSON.stringify(e)), i(e)
			},
			o = function(e) {
				return r.version >= 64 ? e : {
					name: {
						PermissionDeniedError: "NotAllowedError",
						PermissionDismissedError: "NotAllowedError",
						InvalidStateError: "NotAllowedError",
						DevicesNotFoundError: "NotFoundError",
						ConstraintNotSatisfiedError: "OverconstrainedError",
						TrackStartError: "NotReadableError",
						MediaDeviceFailedDueToShutdown: "NotAllowedError",
						MediaDeviceKillSwitchOn: "NotAllowedError",
						TabCaptureError: "AbortError",
						ScreenCaptureError: "AbortError",
						DeviceCaptureError: "AbortError"
					} [e.name] || e.name,
					message: e.message,
					constraint: e.constraint || e.constraintName,
					toString() {
						return this.name + (this.message && ": ") + this.message
					}
				}
			};
		if (t.getUserMedia = function(e, r, n) {
				i(e, (e => {
					t.webkitGetUserMedia(e, r, (e => {
						n && n(o(e))
					}))
				}))
			}.bind(t), t.mediaDevices.getUserMedia) {
			const e = t.mediaDevices.getUserMedia.bind(t.mediaDevices);
			t.mediaDevices.getUserMedia = function(t) {
				return i(t, (t => e(t).then((e => {
					if (t.audio && !e.getAudioTracks().length || t.video && !e
						.getVideoTracks().length) throw e.getTracks().forEach((e => {
						e.stop()
					})), new DOMException("", "NotFoundError");
					return e
				}), (e => Promise.reject(o(e))))))
			}
		}
	}

	function K(e) {
		e.MediaStream = e.MediaStream || e.webkitMediaStream
	}

	function Q(e) {
		if ("object" == typeof e && e.RTCPeerConnection && !("ontrack" in e.RTCPeerConnection.prototype)) {
			Object.defineProperty(e.RTCPeerConnection.prototype, "ontrack", {
				get() {
					return this._ontrack
				},
				set(e) {
					this._ontrack && this.removeEventListener("track", this._ontrack), this
						.addEventListener("track", this._ontrack = e)
				},
				enumerable: !0,
				configurable: !0
			});
			const t = e.RTCPeerConnection.prototype.setRemoteDescription;
			e.RTCPeerConnection.prototype.setRemoteDescription = function() {
				return this._ontrackpoly || (this._ontrackpoly = t => {
					t.stream.addEventListener("addtrack", (r => {
						let n;
						n = e.RTCPeerConnection.prototype.getReceivers ? this
							.getReceivers().find((e => e.track && e.track.id === r.track
								.id)) : {
								track: r.track
							};
						const i = new Event("track");
						i.track = r.track, i.receiver = n, i.transceiver = {
							receiver: n
						}, i.streams = [t.stream], this.dispatchEvent(i)
					})), t.stream.getTracks().forEach((r => {
						let n;
						n = e.RTCPeerConnection.prototype.getReceivers ? this
							.getReceivers().find((e => e.track && e.track.id === r
							.id)) : {
								track: r
							};
						const i = new Event("track");
						i.track = r, i.receiver = n, i.transceiver = {
							receiver: n
						}, i.streams = [t.stream], this.dispatchEvent(i)
					}))
				}, this.addEventListener("addstream", this._ontrackpoly)), t.apply(this, arguments)
			}
		} else N(e, "track", (e => (e.transceiver || Object.defineProperty(e, "transceiver", {
			value: {
				receiver: e.receiver
			}
		}), e)))
	}

	function $(e) {
		if ("object" == typeof e && e.RTCPeerConnection && !("getSenders" in e.RTCPeerConnection.prototype) &&
			"createDTMFSender" in e.RTCPeerConnection.prototype) {
			const t = function(e, t) {
				return {
					track: t,
					get dtmf() {
						return void 0 === this._dtmf && ("audio" === t.kind ? this._dtmf = e
							.createDTMFSender(t) : this._dtmf = null), this._dtmf
					},
					_pc: e
				}
			};
			if (!e.RTCPeerConnection.prototype.getSenders) {
				e.RTCPeerConnection.prototype.getSenders = function() {
					return this._senders = this._senders || [], this._senders.slice()
				};
				const r = e.RTCPeerConnection.prototype.addTrack;
				e.RTCPeerConnection.prototype.addTrack = function(e, n) {
					let i = r.apply(this, arguments);
					return i || (i = t(this, e), this._senders.push(i)), i
				};
				const n = e.RTCPeerConnection.prototype.removeTrack;
				e.RTCPeerConnection.prototype.removeTrack = function(e) {
					n.apply(this, arguments);
					const t = this._senders.indexOf(e); - 1 !== t && this._senders.splice(t, 1)
				}
			}
			const r = e.RTCPeerConnection.prototype.addStream;
			e.RTCPeerConnection.prototype.addStream = function(e) {
				this._senders = this._senders || [], r.apply(this, [e]), e.getTracks().forEach((e => {
					this._senders.push(t(this, e))
				}))
			};
			const n = e.RTCPeerConnection.prototype.removeStream;
			e.RTCPeerConnection.prototype.removeStream = function(e) {
				this._senders = this._senders || [], n.apply(this, [e]), e.getTracks().forEach((e => {
					const t = this._senders.find((t => t.track === e));
					t && this._senders.splice(this._senders.indexOf(t), 1)
				}))
			}
		} else if ("object" == typeof e && e.RTCPeerConnection && "getSenders" in e.RTCPeerConnection
			.prototype && "createDTMFSender" in e.RTCPeerConnection.prototype && e.RTCRtpSender && !("dtmf" in e
				.RTCRtpSender.prototype)) {
			const t = e.RTCPeerConnection.prototype.getSenders;
			e.RTCPeerConnection.prototype.getSenders = function() {
				const e = t.apply(this, []);
				return e.forEach((e => e._pc = this)), e
			}, Object.defineProperty(e.RTCRtpSender.prototype, "dtmf", {
				get() {
					return void 0 === this._dtmf && ("audio" === this.track.kind ? this._dtmf = this
						._pc.createDTMFSender(this.track) : this._dtmf = null), this._dtmf
				}
			})
		}
	}

	function X(e) {
		if (!e.RTCPeerConnection) return;
		const t = e.RTCPeerConnection.prototype.getStats;
		e.RTCPeerConnection.prototype.getStats = function() {
			const [e, r, n] = arguments;
			if (arguments.length > 0 && "function" == typeof e) return t.apply(this, arguments);
			if (0 === t.length && (0 === arguments.length || "function" != typeof e)) return t.apply(this,
			[]);
			const i = function(e) {
					const t = {};
					return e.result().forEach((e => {
						const r = {
							id: e.id,
							timestamp: e.timestamp,
							type: {
								localcandidate: "local-candidate",
								remotecandidate: "remote-candidate"
							} [e.type] || e.type
						};
						e.names().forEach((t => {
							r[t] = e.stat(t)
						})), t[r.id] = r
					})), t
				},
				o = function(e) {
					return new Map(Object.keys(e).map((t => [t, e[t]])))
				};
			if (arguments.length >= 2) {
				const n = function(e) {
					r(o(i(e)))
				};
				return t.apply(this, [n, e])
			}
			return new Promise(((e, r) => {
				t.apply(this, [function(t) {
					e(o(i(t)))
				}, r])
			})).then(r, n)
		}
	}

	function Z(e) {
		if (!("object" == typeof e && e.RTCPeerConnection && e.RTCRtpSender && e.RTCRtpReceiver)) return;
		if (!("getStats" in e.RTCRtpSender.prototype)) {
			const t = e.RTCPeerConnection.prototype.getSenders;
			t && (e.RTCPeerConnection.prototype.getSenders = function() {
				const e = t.apply(this, []);
				return e.forEach((e => e._pc = this)), e
			});
			const r = e.RTCPeerConnection.prototype.addTrack;
			r && (e.RTCPeerConnection.prototype.addTrack = function() {
				const e = r.apply(this, arguments);
				return e._pc = this, e
			}), e.RTCRtpSender.prototype.getStats = function() {
				const e = this;
				return this._pc.getStats().then((t => W(t, e.track, !0)))
			}
		}
		if (!("getStats" in e.RTCRtpReceiver.prototype)) {
			const t = e.RTCPeerConnection.prototype.getReceivers;
			t && (e.RTCPeerConnection.prototype.getReceivers = function() {
					const e = t.apply(this, []);
					return e.forEach((e => e._pc = this)), e
				}), N(e, "track", (e => (e.receiver._pc = e.srcElement, e))), e.RTCRtpReceiver.prototype
				.getStats = function() {
					const e = this;
					return this._pc.getStats().then((t => W(t, e.track, !1)))
				}
		}
		if (!("getStats" in e.RTCRtpSender.prototype) || !("getStats" in e.RTCRtpReceiver.prototype)) return;
		const t = e.RTCPeerConnection.prototype.getStats;
		e.RTCPeerConnection.prototype.getStats = function() {
			if (arguments.length > 0 && arguments[0] instanceof e.MediaStreamTrack) {
				const e = arguments[0];
				let t, r, n;
				return this.getSenders().forEach((r => {
					r.track === e && (t ? n = !0 : t = r)
				})), this.getReceivers().forEach((t => (t.track === e && (r ? n = !0 : r = t), t
					.track === e))), n || t && r ? Promise.reject(new DOMException(
					"There are more than one sender or receiver for the track.",
					"InvalidAccessError")) : t ? t.getStats() : r ? r.getStats() : Promise.reject(
					new DOMException("There is no sender or receiver for the track.",
						"InvalidAccessError"))
			}
			return t.apply(this, arguments)
		}
	}

	function ee(e) {
		e.RTCPeerConnection.prototype.getLocalStreams = function() {
			return this._shimmedLocalStreams = this._shimmedLocalStreams || {}, Object.keys(this
				._shimmedLocalStreams).map((e => this._shimmedLocalStreams[e][0]))
		};
		const t = e.RTCPeerConnection.prototype.addTrack;
		e.RTCPeerConnection.prototype.addTrack = function(e, r) {
			if (!r) return t.apply(this, arguments);
			this._shimmedLocalStreams = this._shimmedLocalStreams || {};
			const n = t.apply(this, arguments);
			return this._shimmedLocalStreams[r.id] ? -1 === this._shimmedLocalStreams[r.id].indexOf(n) &&
				this._shimmedLocalStreams[r.id].push(n) : this._shimmedLocalStreams[r.id] = [r, n], n
		};
		const r = e.RTCPeerConnection.prototype.addStream;
		e.RTCPeerConnection.prototype.addStream = function(e) {
			this._shimmedLocalStreams = this._shimmedLocalStreams || {}, e.getTracks().forEach((e => {
				if (this.getSenders().find((t => t.track === e))) throw new DOMException(
					"Track already exists.", "InvalidAccessError")
			}));
			const t = this.getSenders();
			r.apply(this, arguments);
			const n = this.getSenders().filter((e => -1 === t.indexOf(e)));
			this._shimmedLocalStreams[e.id] = [e].concat(n)
		};
		const n = e.RTCPeerConnection.prototype.removeStream;
		e.RTCPeerConnection.prototype.removeStream = function(e) {
			return this._shimmedLocalStreams = this._shimmedLocalStreams || {}, delete this
				._shimmedLocalStreams[e.id], n.apply(this, arguments)
		};
		const i = e.RTCPeerConnection.prototype.removeTrack;
		e.RTCPeerConnection.prototype.removeTrack = function(e) {
			return this._shimmedLocalStreams = this._shimmedLocalStreams || {}, e && Object.keys(this
				._shimmedLocalStreams).forEach((t => {
				const r = this._shimmedLocalStreams[t].indexOf(e); - 1 !== r && this
					._shimmedLocalStreams[t].splice(r, 1), 1 === this._shimmedLocalStreams[t]
					.length && delete this._shimmedLocalStreams[t]
			})), i.apply(this, arguments)
		}
	}

	function te(e) {
		if (!e.RTCPeerConnection) return;
		const t = V(e);
		if (e.RTCPeerConnection.prototype.addTrack && t.version >= 65) return ee(e);
		const r = e.RTCPeerConnection.prototype.getLocalStreams;
		e.RTCPeerConnection.prototype.getLocalStreams = function() {
			const e = r.apply(this);
			return this._reverseStreams = this._reverseStreams || {}, e.map((e => this._reverseStreams[e
				.id]))
		};
		const n = e.RTCPeerConnection.prototype.addStream;
		e.RTCPeerConnection.prototype.addStream = function(t) {
			if (this._streams = this._streams || {}, this._reverseStreams = this._reverseStreams || {}, t
				.getTracks().forEach((e => {
					if (this.getSenders().find((t => t.track === e))) throw new DOMException(
						"Track already exists.", "InvalidAccessError")
				})), !this._reverseStreams[t.id]) {
				const r = new e.MediaStream(t.getTracks());
				this._streams[t.id] = r, this._reverseStreams[r.id] = t, t = r
			}
			n.apply(this, [t])
		};
		const i = e.RTCPeerConnection.prototype.removeStream;

		function o(e, t) {
			let r = t.sdp;
			return Object.keys(e._reverseStreams || []).forEach((t => {
				const n = e._reverseStreams[t],
					i = e._streams[n.id];
				r = r.replace(new RegExp(i.id, "g"), n.id)
			})), new RTCSessionDescription({
				type: t.type,
				sdp: r
			})
		}

		function s(e, t) {
			let r = t.sdp;
			return Object.keys(e._reverseStreams || []).forEach((t => {
				const n = e._reverseStreams[t],
					i = e._streams[n.id];
				r = r.replace(new RegExp(n.id, "g"), i.id)
			})), new RTCSessionDescription({
				type: t.type,
				sdp: r
			})
		}
		e.RTCPeerConnection.prototype.removeStream = function(e) {
			this._streams = this._streams || {}, this._reverseStreams = this._reverseStreams || {}, i.apply(
				this, [this._streams[e.id] || e]), delete this._reverseStreams[this._streams[e.id] ?
				this._streams[e.id].id : e.id], delete this._streams[e.id]
		}, e.RTCPeerConnection.prototype.addTrack = function(t, r) {
			if ("closed" === this.signalingState) throw new DOMException(
				"The RTCPeerConnection's signalingState is 'closed'.", "InvalidStateError");
			const n = [].slice.call(arguments, 1);
			if (1 !== n.length || !n[0].getTracks().find((e => e === t))) throw new DOMException(
				"The adapter.js addTrack polyfill only supports a single  stream which is associated with the specified track.",
				"NotSupportedError");
			const i = this.getSenders().find((e => e.track === t));
			if (i) throw new DOMException("Track already exists.", "InvalidAccessError");
			this._streams = this._streams || {}, this._reverseStreams = this._reverseStreams || {};
			const o = this._streams[r.id];
			if (o) o.addTrack(t), Promise.resolve().then((() => {
				this.dispatchEvent(new Event("negotiationneeded"))
			}));
			else {
				const n = new e.MediaStream([t]);
				this._streams[r.id] = n, this._reverseStreams[n.id] = r, this.addStream(n)
			}
			return this.getSenders().find((e => e.track === t))
		}, ["createOffer", "createAnswer"].forEach((function(t) {
			const r = e.RTCPeerConnection.prototype[t],
				n = {
					[t]() {
						const e = arguments;
						return arguments.length && "function" == typeof arguments[0] ? r.apply(this,
							[t => {
								const r = o(this, t);
								e[0].apply(null, [r])
							}, t => {
								e[1] && e[1].apply(null, t)
							}, arguments[2]]) : r.apply(this, arguments).then((e => o(this, e)))
					}
				};
			e.RTCPeerConnection.prototype[t] = n[t]
		}));
		const a = e.RTCPeerConnection.prototype.setLocalDescription;
		e.RTCPeerConnection.prototype.setLocalDescription = function() {
			return arguments.length && arguments[0].type ? (arguments[0] = s(this, arguments[0]), a.apply(
				this, arguments)) : a.apply(this, arguments)
		};
		const c = Object.getOwnPropertyDescriptor(e.RTCPeerConnection.prototype, "localDescription");
		Object.defineProperty(e.RTCPeerConnection.prototype, "localDescription", {
			get() {
				const e = c.get.apply(this);
				return "" === e.type ? e : o(this, e)
			}
		}), e.RTCPeerConnection.prototype.removeTrack = function(e) {
			if ("closed" === this.signalingState) throw new DOMException(
				"The RTCPeerConnection's signalingState is 'closed'.", "InvalidStateError");
			if (!e._pc) throw new DOMException(
				"Argument 1 of RTCPeerConnection.removeTrack does not implement interface RTCRtpSender.",
				"TypeError");
			if (!(e._pc === this)) throw new DOMException("Sender was not created by this connection.",
				"InvalidAccessError");
			let t;
			this._streams = this._streams || {}, Object.keys(this._streams).forEach((r => {
				this._streams[r].getTracks().find((t => e.track === t)) && (t = this._streams[
					r])
			})), t && (1 === t.getTracks().length ? this.removeStream(this._reverseStreams[t.id]) : t
				.removeTrack(e.track), this.dispatchEvent(new Event("negotiationneeded")))
		}
	}

	function re(e) {
		const t = V(e);
		if (!e.RTCPeerConnection && e.webkitRTCPeerConnection && (e.RTCPeerConnection = e
				.webkitRTCPeerConnection), !e.RTCPeerConnection) return;
		const r = 0 === e.RTCPeerConnection.prototype.addIceCandidate.length;
		t.version < 53 && ["setLocalDescription", "setRemoteDescription", "addIceCandidate"].forEach((function(
			t) {
			const r = e.RTCPeerConnection.prototype[t],
				n = {
					[t]() {
						return arguments[0] = new("addIceCandidate" === t ? e.RTCIceCandidate : e
							.RTCSessionDescription)(arguments[0]), r.apply(this, arguments)
					}
				};
			e.RTCPeerConnection.prototype[t] = n[t]
		}));
		const n = e.RTCPeerConnection.prototype.addIceCandidate;
		e.RTCPeerConnection.prototype.addIceCandidate = function() {
			return r || arguments[0] ? t.version < 78 && arguments[0] && "" === arguments[0].candidate ?
				Promise.resolve() : n.apply(this, arguments) : (arguments[1] && arguments[1].apply(null),
					Promise.resolve())
		}
	}

	function ne(e) {
		const t = V(e);
		N(e, "negotiationneeded", (e => {
			const r = e.target;
			if (!(t.version < 72 || r.getConfiguration && "plan-b" === r.getConfiguration()
					.sdpSemantics) || "stable" === r.signalingState) return e
		}))
	}
	var ie = Object.freeze({
		__proto__: null,
		shimMediaStream: K,
		shimOnTrack: Q,
		shimGetSendersWithDtmf: $,
		shimGetStats: X,
		shimSenderReceiverGetStats: Z,
		shimAddTrackRemoveTrackWithNative: ee,
		shimAddTrackRemoveTrack: te,
		shimPeerConnection: re,
		fixNegotiationNeeded: ne,
		shimGetUserMedia: Y,
		shimGetDisplayMedia: function(e, t) {
			e.navigator.mediaDevices && "getDisplayMedia" in e.navigator.mediaDevices || e.navigator
				.mediaDevices && ("function" == typeof t ? e.navigator.mediaDevices
					.getDisplayMedia = function(r) {
						return t(r).then((t => {
							const n = r.video && r.video.width,
								i = r.video && r.video.height,
								o = r.video && r.video.frameRate;
							return r.video = {
									mandatory: {
										chromeMediaSource: "desktop",
										chromeMediaSourceId: t,
										maxFrameRate: o || 3
									}
								}, n && (r.video.mandatory.maxWidth = n), i && (r.video
									.mandatory.maxHeight = i), e.navigator.mediaDevices
								.getUserMedia(r)
						}))
					} : console.error("shimGetDisplayMedia: getSourceId argument is not a function")
					)
		}
	});
	var oe = d((function(e) {
		var t = {
			generateIdentifier: function() {
				return Math.random().toString(36).substr(2, 10)
			}
		};
		t.localCName = t.generateIdentifier(), t.splitLines = function(e) {
			return e.trim().split("\n").map((function(e) {
				return e.trim()
			}))
		}, t.splitSections = function(e) {
			return e.split("\nm=").map((function(e, t) {
				return (t > 0 ? "m=" + e : e).trim() + "\r\n"
			}))
		}, t.getDescription = function(e) {
			var r = t.splitSections(e);
			return r && r[0]
		}, t.getMediaSections = function(e) {
			var r = t.splitSections(e);
			return r.shift(), r
		}, t.matchPrefix = function(e, r) {
			return t.splitLines(e).filter((function(e) {
				return 0 === e.indexOf(r)
			}))
		}, t.parseCandidate = function(e) {
			for (var t, r = {
					foundation: (t = 0 === e.indexOf("a=candidate:") ? e.substring(12)
						.split(" ") : e.substring(10).split(" "))[0],
					component: parseInt(t[1], 10),
					protocol: t[2].toLowerCase(),
					priority: parseInt(t[3], 10),
					ip: t[4],
					address: t[4],
					port: parseInt(t[5], 10),
					type: t[7]
				}, n = 8; n < t.length; n += 2) switch (t[n]) {
				case "raddr":
					r.relatedAddress = t[n + 1];
					break;
				case "rport":
					r.relatedPort = parseInt(t[n + 1], 10);
					break;
				case "tcptype":
					r.tcpType = t[n + 1];
					break;
				case "ufrag":
					r.ufrag = t[n + 1], r.usernameFragment = t[n + 1];
					break;
				default:
					r[t[n]] = t[n + 1]
			}
			return r
		}, t.writeCandidate = function(e) {
			var t = [];
			t.push(e.foundation), t.push(e.component), t.push(e.protocol.toUpperCase()), t.push(
				e.priority), t.push(e.address || e.ip), t.push(e.port);
			var r = e.type;
			return t.push("typ"), t.push(r), "host" !== r && e.relatedAddress && e
				.relatedPort && (t.push("raddr"), t.push(e.relatedAddress), t.push("rport"), t
					.push(e.relatedPort)), e.tcpType && "tcp" === e.protocol.toLowerCase() && (t
					.push("tcptype"), t.push(e.tcpType)), (e.usernameFragment || e.ufrag) && (t
					.push("ufrag"), t.push(e.usernameFragment || e.ufrag)), "candidate:" + t
				.join(" ")
		}, t.parseIceOptions = function(e) {
			return e.substr(14).split(" ")
		}, t.parseRtpMap = function(e) {
			var t = e.substr(9).split(" "),
				r = {
					payloadType: parseInt(t.shift(), 10)
				};
			return t = t[0].split("/"), r.name = t[0], r.clockRate = parseInt(t[1], 10), r
				.channels = 3 === t.length ? parseInt(t[2], 10) : 1, r.numChannels = r.channels,
				r
		}, t.writeRtpMap = function(e) {
			var t = e.payloadType;
			void 0 !== e.preferredPayloadType && (t = e.preferredPayloadType);
			var r = e.channels || e.numChannels || 1;
			return "a=rtpmap:" + t + " " + e.name + "/" + e.clockRate + (1 !== r ? "/" + r :
				"") + "\r\n"
		}, t.parseExtmap = function(e) {
			var t = e.substr(9).split(" ");
			return {
				id: parseInt(t[0], 10),
				direction: t[0].indexOf("/") > 0 ? t[0].split("/")[1] : "sendrecv",
				uri: t[1]
			}
		}, t.writeExtmap = function(e) {
			return "a=extmap:" + (e.id || e.preferredId) + (e.direction && "sendrecv" !== e
				.direction ? "/" + e.direction : "") + " " + e.uri + "\r\n"
		}, t.parseFmtp = function(e) {
			for (var t, r = {}, n = e.substr(e.indexOf(" ") + 1).split(";"), i = 0; i < n
				.length; i++) r[(t = n[i].trim().split("="))[0].trim()] = t[1];
			return r
		}, t.writeFmtp = function(e) {
			var t = "",
				r = e.payloadType;
			if (void 0 !== e.preferredPayloadType && (r = e.preferredPayloadType), e
				.parameters && Object.keys(e.parameters).length) {
				var n = [];
				Object.keys(e.parameters).forEach((function(t) {
					e.parameters[t] ? n.push(t + "=" + e.parameters[t]) : n.push(t)
				})), t += "a=fmtp:" + r + " " + n.join(";") + "\r\n"
			}
			return t
		}, t.parseRtcpFb = function(e) {
			var t = e.substr(e.indexOf(" ") + 1).split(" ");
			return {
				type: t.shift(),
				parameter: t.join(" ")
			}
		}, t.writeRtcpFb = function(e) {
			var t = "",
				r = e.payloadType;
			return void 0 !== e.preferredPayloadType && (r = e.preferredPayloadType), e
				.rtcpFeedback && e.rtcpFeedback.length && e.rtcpFeedback.forEach((function(e) {
					t += "a=rtcp-fb:" + r + " " + e.type + (e.parameter && e.parameter
						.length ? " " + e.parameter : "") + "\r\n"
				})), t
		}, t.parseSsrcMedia = function(e) {
			var t = e.indexOf(" "),
				r = {
					ssrc: parseInt(e.substr(7, t - 7), 10)
				},
				n = e.indexOf(":", t);
			return n > -1 ? (r.attribute = e.substr(t + 1, n - t - 1), r.value = e.substr(n +
				1)) : r.attribute = e.substr(t + 1), r
		}, t.parseSsrcGroup = function(e) {
			var t = e.substr(13).split(" ");
			return {
				semantics: t.shift(),
				ssrcs: t.map((function(e) {
					return parseInt(e, 10)
				}))
			}
		}, t.getMid = function(e) {
			var r = t.matchPrefix(e, "a=mid:")[0];
			if (r) return r.substr(6)
		}, t.parseFingerprint = function(e) {
			var t = e.substr(14).split(" ");
			return {
				algorithm: t[0].toLowerCase(),
				value: t[1]
			}
		}, t.getDtlsParameters = function(e, r) {
			return {
				role: "auto",
				fingerprints: t.matchPrefix(e + r, "a=fingerprint:").map(t.parseFingerprint)
			}
		}, t.writeDtlsParameters = function(e, t) {
			var r = "a=setup:" + t + "\r\n";
			return e.fingerprints.forEach((function(e) {
				r += "a=fingerprint:" + e.algorithm + " " + e.value + "\r\n"
			})), r
		}, t.parseCryptoLine = function(e) {
			var t = e.substr(9).split(" ");
			return {
				tag: parseInt(t[0], 10),
				cryptoSuite: t[1],
				keyParams: t[2],
				sessionParams: t.slice(3)
			}
		}, t.writeCryptoLine = function(e) {
			return "a=crypto:" + e.tag + " " + e.cryptoSuite + " " + ("object" == typeof e
				.keyParams ? t.writeCryptoKeyParams(e.keyParams) : e.keyParams) + (e
				.sessionParams ? " " + e.sessionParams.join(" ") : "") + "\r\n"
		}, t.parseCryptoKeyParams = function(e) {
			if (0 !== e.indexOf("inline:")) return null;
			var t = e.substr(7).split("|");
			return {
				keyMethod: "inline",
				keySalt: t[0],
				lifeTime: t[1],
				mkiValue: t[2] ? t[2].split(":")[0] : void 0,
				mkiLength: t[2] ? t[2].split(":")[1] : void 0
			}
		}, t.writeCryptoKeyParams = function(e) {
			return e.keyMethod + ":" + e.keySalt + (e.lifeTime ? "|" + e.lifeTime : "") + (e
				.mkiValue && e.mkiLength ? "|" + e.mkiValue + ":" + e.mkiLength : "")
		}, t.getCryptoParameters = function(e, r) {
			return t.matchPrefix(e + r, "a=crypto:").map(t.parseCryptoLine)
		}, t.getIceParameters = function(e, r) {
			var n = t.matchPrefix(e + r, "a=ice-ufrag:")[0],
				i = t.matchPrefix(e + r, "a=ice-pwd:")[0];
			return n && i ? {
				usernameFragment: n.substr(12),
				password: i.substr(10)
			} : null
		}, t.writeIceParameters = function(e) {
			return "a=ice-ufrag:" + e.usernameFragment + "\r\na=ice-pwd:" + e.password + "\r\n"
		}, t.parseRtpParameters = function(e) {
			for (var r = {
					codecs: [],
					headerExtensions: [],
					fecMechanisms: [],
					rtcp: []
				}, n = t.splitLines(e)[0].split(" "), i = 3; i < n.length; i++) {
				var o = n[i],
					s = t.matchPrefix(e, "a=rtpmap:" + o + " ")[0];
				if (s) {
					var a = t.parseRtpMap(s),
						c = t.matchPrefix(e, "a=fmtp:" + o + " ");
					switch (a.parameters = c.length ? t.parseFmtp(c[0]) : {}, a.rtcpFeedback = t
						.matchPrefix(e, "a=rtcp-fb:" + o + " ").map(t.parseRtcpFb), r.codecs
						.push(a), a.name.toUpperCase()) {
						case "RED":
						case "ULPFEC":
							r.fecMechanisms.push(a.name.toUpperCase())
					}
				}
			}
			return t.matchPrefix(e, "a=extmap:").forEach((function(e) {
				r.headerExtensions.push(t.parseExtmap(e))
			})), r
		}, t.writeRtpDescription = function(e, r) {
			var n = "";
			n += "m=" + e + " ", n += r.codecs.length > 0 ? "9" : "0", n +=
				" UDP/TLS/RTP/SAVPF ", n += r.codecs.map((function(e) {
					return void 0 !== e.preferredPayloadType ? e.preferredPayloadType :
						e.payloadType
				})).join(" ") + "\r\n", n += "c=IN IP4 0.0.0.0\r\n", n +=
				"a=rtcp:9 IN IP4 0.0.0.0\r\n", r.codecs.forEach((function(e) {
					n += t.writeRtpMap(e), n += t.writeFmtp(e), n += t.writeRtcpFb(e)
				}));
			var i = 0;
			return r.codecs.forEach((function(e) {
					e.maxptime > i && (i = e.maxptime)
				})), i > 0 && (n += "a=maxptime:" + i + "\r\n"), n += "a=rtcp-mux\r\n", r
				.headerExtensions && r.headerExtensions.forEach((function(e) {
					n += t.writeExtmap(e)
				})), n
		}, t.parseRtpEncodingParameters = function(e) {
			var r, n = [],
				i = t.parseRtpParameters(e),
				o = -1 !== i.fecMechanisms.indexOf("RED"),
				s = -1 !== i.fecMechanisms.indexOf("ULPFEC"),
				a = t.matchPrefix(e, "a=ssrc:").map((function(e) {
					return t.parseSsrcMedia(e)
				})).filter((function(e) {
					return "cname" === e.attribute
				})),
				c = a.length > 0 && a[0].ssrc,
				d = t.matchPrefix(e, "a=ssrc-group:FID").map((function(e) {
					return e.substr(17).split(" ").map((function(e) {
						return parseInt(e, 10)
					}))
				}));
			d.length > 0 && d[0].length > 1 && d[0][0] === c && (r = d[0][1]), i.codecs.forEach(
				(function(e) {
					if ("RTX" === e.name.toUpperCase() && e.parameters.apt) {
						var t = {
							ssrc: c,
							codecPayloadType: parseInt(e.parameters.apt, 10)
						};
						c && r && (t.rtx = {
							ssrc: r
						}), n.push(t), o && ((t = JSON.parse(JSON.stringify(t)))
							.fec = {
								ssrc: c,
								mechanism: s ? "red+ulpfec" : "red"
							}, n.push(t))
					}
				})), 0 === n.length && c && n.push({
				ssrc: c
			});
			var p = t.matchPrefix(e, "b=");
			return p.length && (p = 0 === p[0].indexOf("b=TIAS:") ? parseInt(p[0].substr(7),
				10) : 0 === p[0].indexOf("b=AS:") ? 1e3 * parseInt(p[0].substr(5), 10) *
				.95 - 16e3 : void 0, n.forEach((function(e) {
					e.maxBitrate = p
				}))), n
		}, t.parseRtcpParameters = function(e) {
			var r = {},
				n = t.matchPrefix(e, "a=ssrc:").map((function(e) {
					return t.parseSsrcMedia(e)
				})).filter((function(e) {
					return "cname" === e.attribute
				}))[0];
			n && (r.cname = n.value, r.ssrc = n.ssrc);
			var i = t.matchPrefix(e, "a=rtcp-rsize");
			r.reducedSize = i.length > 0, r.compound = 0 === i.length;
			var o = t.matchPrefix(e, "a=rtcp-mux");
			return r.mux = o.length > 0, r
		}, t.parseMsid = function(e) {
			var r, n = t.matchPrefix(e, "a=msid:");
			if (1 === n.length) return {
				stream: (r = n[0].substr(7).split(" "))[0],
				track: r[1]
			};
			var i = t.matchPrefix(e, "a=ssrc:").map((function(e) {
				return t.parseSsrcMedia(e)
			})).filter((function(e) {
				return "msid" === e.attribute
			}));
			return i.length > 0 ? {
				stream: (r = i[0].value.split(" "))[0],
				track: r[1]
			} : void 0
		}, t.parseSctpDescription = function(e) {
			var r, n = t.parseMLine(e),
				i = t.matchPrefix(e, "a=max-message-size:");
			i.length > 0 && (r = parseInt(i[0].substr(19), 10)), isNaN(r) && (r = 65536);
			var o = t.matchPrefix(e, "a=sctp-port:");
			if (o.length > 0) return {
				port: parseInt(o[0].substr(12), 10),
				protocol: n.fmt,
				maxMessageSize: r
			};
			if (t.matchPrefix(e, "a=sctpmap:").length > 0) {
				var s = t.matchPrefix(e, "a=sctpmap:")[0].substr(10).split(" ");
				return {
					port: parseInt(s[0], 10),
					protocol: s[1],
					maxMessageSize: r
				}
			}
		}, t.writeSctpDescription = function(e, t) {
			var r = [];
			return r = "DTLS/SCTP" !== e.protocol ? ["m=" + e.kind + " 9 " + e.protocol + " " +
				t.protocol + "\r\n", "c=IN IP4 0.0.0.0\r\n", "a=sctp-port:" + t.port +
				"\r\n"
			] : ["m=" + e.kind + " 9 " + e.protocol + " " + t.port + "\r\n",
				"c=IN IP4 0.0.0.0\r\n", "a=sctpmap:" + t.port + " " + t.protocol +
				" 65535\r\n"
			], void 0 !== t.maxMessageSize && r.push("a=max-message-size:" + t
				.maxMessageSize + "\r\n"), r.join("")
		}, t.generateSessionId = function() {
			return Math.random().toString().substr(2, 21)
		}, t.writeSessionBoilerplate = function(e, r, n) {
			var i = void 0 !== r ? r : 2;
			return "v=0\r\no=" + (n || "thisisadapterortc") + " " + (e || t
			.generateSessionId()) + " " + i + " IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\n"
		}, t.writeMediaSection = function(e, r, n, i) {
			var o = t.writeRtpDescription(e.kind, r);
			if (o += t.writeIceParameters(e.iceGatherer.getLocalParameters()), o += t
				.writeDtlsParameters(e.dtlsTransport.getLocalParameters(), "offer" === n ?
					"actpass" : "active"), o += "a=mid:" + e.mid + "\r\n", e.direction ? o +=
				"a=" + e.direction + "\r\n" : e.rtpSender && e.rtpReceiver ? o +=
				"a=sendrecv\r\n" : e.rtpSender ? o += "a=sendonly\r\n" : e.rtpReceiver ? o +=
				"a=recvonly\r\n" : o += "a=inactive\r\n", e.rtpSender) {
				var s = "msid:" + i.id + " " + e.rtpSender.track.id + "\r\n";
				o += "a=" + s, o += "a=ssrc:" + e.sendEncodingParameters[0].ssrc + " " + s, e
					.sendEncodingParameters[0].rtx && (o += "a=ssrc:" + e
						.sendEncodingParameters[0].rtx.ssrc + " " + s, o +=
						"a=ssrc-group:FID " + e.sendEncodingParameters[0].ssrc + " " + e
						.sendEncodingParameters[0].rtx.ssrc + "\r\n")
			}
			return o += "a=ssrc:" + e.sendEncodingParameters[0].ssrc + " cname:" + t
				.localCName + "\r\n", e.rtpSender && e.sendEncodingParameters[0].rtx && (o +=
					"a=ssrc:" + e.sendEncodingParameters[0].rtx.ssrc + " cname:" + t
					.localCName + "\r\n"), o
		}, t.getDirection = function(e, r) {
			for (var n = t.splitLines(e), i = 0; i < n.length; i++) switch (n[i]) {
				case "a=sendrecv":
				case "a=sendonly":
				case "a=recvonly":
				case "a=inactive":
					return n[i].substr(2)
			}
			return r ? t.getDirection(r) : "sendrecv"
		}, t.getKind = function(e) {
			return t.splitLines(e)[0].split(" ")[0].substr(2)
		}, t.isRejected = function(e) {
			return "0" === e.split(" ", 2)[1]
		}, t.parseMLine = function(e) {
			var r = t.splitLines(e)[0].substr(2).split(" ");
			return {
				kind: r[0],
				port: parseInt(r[1], 10),
				protocol: r[2],
				fmt: r.slice(3).join(" ")
			}
		}, t.parseOLine = function(e) {
			var r = t.matchPrefix(e, "o=")[0].substr(2).split(" ");
			return {
				username: r[0],
				sessionId: r[1],
				sessionVersion: parseInt(r[2], 10),
				netType: r[3],
				addressType: r[4],
				address: r[5]
			}
		}, t.isValidSDP = function(e) {
			if ("string" != typeof e || 0 === e.length) return !1;
			for (var r = t.splitLines(e), n = 0; n < r.length; n++)
				if (r[n].length < 2 || "=" !== r[n].charAt(1)) return !1;
			return !0
		}, e.exports = t
	}));

	function se(e, t, r, n, i) {
		var o = oe.writeRtpDescription(e.kind, t);
		if (o += oe.writeIceParameters(e.iceGatherer.getLocalParameters()), o += oe.writeDtlsParameters(e
				.dtlsTransport.getLocalParameters(), "offer" === r ? "actpass" : i || "active"), o += "a=mid:" +
			e.mid + "\r\n", e.rtpSender && e.rtpReceiver ? o += "a=sendrecv\r\n" : e.rtpSender ? o +=
			"a=sendonly\r\n" : e.rtpReceiver ? o += "a=recvonly\r\n" : o += "a=inactive\r\n", e.rtpSender) {
			var s = e.rtpSender._initialTrackId || e.rtpSender.track.id;
			e.rtpSender._initialTrackId = s;
			var a = "msid:" + (n ? n.id : "-") + " " + s + "\r\n";
			o += "a=" + a, o += "a=ssrc:" + e.sendEncodingParameters[0].ssrc + " " + a, e
				.sendEncodingParameters[0].rtx && (o += "a=ssrc:" + e.sendEncodingParameters[0].rtx.ssrc + " " +
					a, o += "a=ssrc-group:FID " + e.sendEncodingParameters[0].ssrc + " " + e
					.sendEncodingParameters[0].rtx.ssrc + "\r\n")
		}
		return o += "a=ssrc:" + e.sendEncodingParameters[0].ssrc + " cname:" + oe.localCName + "\r\n", e
			.rtpSender && e.sendEncodingParameters[0].rtx && (o += "a=ssrc:" + e.sendEncodingParameters[0].rtx
				.ssrc + " cname:" + oe.localCName + "\r\n"), o
	}

	function ae(e, t) {
		var r = {
				codecs: [],
				headerExtensions: [],
				fecMechanisms: []
			},
			n = function(e, t) {
				e = parseInt(e, 10);
				for (var r = 0; r < t.length; r++)
					if (t[r].payloadType === e || t[r].preferredPayloadType === e) return t[r]
			},
			i = function(e, t, r, i) {
				var o = n(e.parameters.apt, r),
					s = n(t.parameters.apt, i);
				return o && s && o.name.toLowerCase() === s.name.toLowerCase()
			};
		return e.codecs.forEach((function(n) {
			for (var o = 0; o < t.codecs.length; o++) {
				var s = t.codecs[o];
				if (n.name.toLowerCase() === s.name.toLowerCase() && n.clockRate === s.clockRate) {
					if ("rtx" === n.name.toLowerCase() && n.parameters && s.parameters.apt && !i(n,
							s, e.codecs, t.codecs)) continue;
					(s = JSON.parse(JSON.stringify(s))).numChannels = Math.min(n.numChannels, s
						.numChannels), r.codecs.push(s), s.rtcpFeedback = s.rtcpFeedback.filter(
						(function(e) {
							for (var t = 0; t < n.rtcpFeedback.length; t++)
								if (n.rtcpFeedback[t].type === e.type && n.rtcpFeedback[t]
									.parameter === e.parameter) return !0;
							return !1
						}));
					break
				}
			}
		})), e.headerExtensions.forEach((function(e) {
			for (var n = 0; n < t.headerExtensions.length; n++) {
				var i = t.headerExtensions[n];
				if (e.uri === i.uri) {
					r.headerExtensions.push(i);
					break
				}
			}
		})), r
	}

	function ce(e, t, r) {
		return -1 !== {
			offer: {
				setLocalDescription: ["stable", "have-local-offer"],
				setRemoteDescription: ["stable", "have-remote-offer"]
			},
			answer: {
				setLocalDescription: ["have-remote-offer", "have-local-pranswer"],
				setRemoteDescription: ["have-local-offer", "have-remote-pranswer"]
			}
		} [t][e].indexOf(r)
	}

	function de(e, t) {
		var r = e.getRemoteCandidates().find((function(e) {
			return t.foundation === e.foundation && t.ip === e.ip && t.port === e.port && t
				.priority === e.priority && t.protocol === e.protocol && t.type === e.type
		}));
		return r || e.addRemoteCandidate(t), !r
	}

	function pe(e, t) {
		var r = new Error(t);
		return r.name = e, r.code = {
			NotSupportedError: 9,
			InvalidStateError: 11,
			InvalidAccessError: 15,
			TypeError: void 0,
			OperationError: void 0
		} [e], r
	}
	var le = function(e, t) {
		function r(t, r) {
			r.addTrack(t), r.dispatchEvent(new e.MediaStreamTrackEvent("addtrack", {
				track: t
			}))
		}

		function n(t, r, n, i) {
			var o = new Event("track");
			o.track = r, o.receiver = n, o.transceiver = {
				receiver: n
			}, o.streams = i, e.setTimeout((function() {
				t._dispatchEvent("track", o)
			}))
		}
		var i = function(r) {
			var n = this,
				i = document.createDocumentFragment();
			if (["addEventListener", "removeEventListener", "dispatchEvent"].forEach((function(e) {
					n[e] = i[e].bind(i)
				})), this.canTrickleIceCandidates = null, this.needNegotiation = !1, this
				.localStreams = [], this.remoteStreams = [], this._localDescription = null, this
				._remoteDescription = null, this.signalingState = "stable", this.iceConnectionState =
				"new", this.connectionState = "new", this.iceGatheringState = "new", r = JSON.parse(JSON
					.stringify(r || {})), this.usingBundle = "max-bundle" === r.bundlePolicy,
				"negotiate" === r.rtcpMuxPolicy) throw pe("NotSupportedError",
				"rtcpMuxPolicy 'negotiate' is not supported");
			switch (r.rtcpMuxPolicy || (r.rtcpMuxPolicy = "require"), r.iceTransportPolicy) {
				case "all":
				case "relay":
					break;
				default:
					r.iceTransportPolicy = "all"
			}
			switch (r.bundlePolicy) {
				case "balanced":
				case "max-compat":
				case "max-bundle":
					break;
				default:
					r.bundlePolicy = "balanced"
			}
			if (r.iceServers = function(e, t) {
					var r = !1;
					return (e = JSON.parse(JSON.stringify(e))).filter((function(e) {
						if (e && (e.urls || e.url)) {
							var n = e.urls || e.url;
							e.url && !e.urls && console.warn(
								"RTCIceServer.url is deprecated! Use urls instead.");
							var i = "string" == typeof n;
							return i && (n = [n]), n = n.filter((function(e) {
								return 0 !== e.indexOf("turn:") || -1 === e
									.indexOf("transport=udp") || -1 !== e
									.indexOf("turn:[") || r ? 0 === e.indexOf(
										"stun:") && t >= 14393 && -1 === e
									.indexOf("?transport=udp") : (r = !0, !0)
							})), delete e.url, e.urls = i ? n[0] : n, !!n.length
						}
					}))
				}(r.iceServers || [], t), this._iceGatherers = [], r.iceCandidatePoolSize)
				for (var o = r.iceCandidatePoolSize; o > 0; o--) this._iceGatherers.push(new e
					.RTCIceGatherer({
						iceServers: r.iceServers,
						gatherPolicy: r.iceTransportPolicy
					}));
			else r.iceCandidatePoolSize = 0;
			this._config = r, this.transceivers = [], this._sdpSessionId = oe.generateSessionId(), this
				._sdpSessionVersion = 0, this._dtlsRole = void 0, this._isClosed = !1
		};
		Object.defineProperty(i.prototype, "localDescription", {
				configurable: !0,
				get: function() {
					return this._localDescription
				}
			}), Object.defineProperty(i.prototype, "remoteDescription", {
				configurable: !0,
				get: function() {
					return this._remoteDescription
				}
			}), i.prototype.onicecandidate = null, i.prototype.onaddstream = null, i.prototype.ontrack =
			null, i.prototype.onremovestream = null, i.prototype.onsignalingstatechange = null, i.prototype
			.oniceconnectionstatechange = null, i.prototype.onconnectionstatechange = null, i.prototype
			.onicegatheringstatechange = null, i.prototype.onnegotiationneeded = null, i.prototype
			.ondatachannel = null, i.prototype._dispatchEvent = function(e, t) {
				this._isClosed || (this.dispatchEvent(t), "function" == typeof this["on" + e] && this["on" +
					e](t))
			}, i.prototype._emitGatheringStateChange = function() {
				var e = new Event("icegatheringstatechange");
				this._dispatchEvent("icegatheringstatechange", e)
			}, i.prototype.getConfiguration = function() {
				return this._config
			}, i.prototype.getLocalStreams = function() {
				return this.localStreams
			}, i.prototype.getRemoteStreams = function() {
				return this.remoteStreams
			}, i.prototype._createTransceiver = function(e, t) {
				var r = this.transceivers.length > 0,
					n = {
						track: null,
						iceGatherer: null,
						iceTransport: null,
						dtlsTransport: null,
						localCapabilities: null,
						remoteCapabilities: null,
						rtpSender: null,
						rtpReceiver: null,
						kind: e,
						mid: null,
						sendEncodingParameters: null,
						recvEncodingParameters: null,
						stream: null,
						associatedRemoteMediaStreams: [],
						wantReceive: !0
					};
				if (this.usingBundle && r) n.iceTransport = this.transceivers[0].iceTransport, n
					.dtlsTransport = this.transceivers[0].dtlsTransport;
				else {
					var i = this._createIceAndDtlsTransports();
					n.iceTransport = i.iceTransport, n.dtlsTransport = i.dtlsTransport
				}
				return t || this.transceivers.push(n), n
			}, i.prototype.addTrack = function(t, r) {
				if (this._isClosed) throw pe("InvalidStateError",
					"Attempted to call addTrack on a closed peerconnection.");
				var n;
				if (this.transceivers.find((function(e) {
						return e.track === t
					}))) throw pe("InvalidAccessError", "Track already exists.");
				for (var i = 0; i < this.transceivers.length; i++) this.transceivers[i].track || this
					.transceivers[i].kind !== t.kind || (n = this.transceivers[i]);
				return n || (n = this._createTransceiver(t.kind)), this._maybeFireNegotiationNeeded(), -
					1 === this.localStreams.indexOf(r) && this.localStreams.push(r), n.track = t, n.stream =
					r, n.rtpSender = new e.RTCRtpSender(t, n.dtlsTransport), n.rtpSender
			}, i.prototype.addStream = function(e) {
				var r = this;
				if (t >= 15025) e.getTracks().forEach((function(t) {
					r.addTrack(t, e)
				}));
				else {
					var n = e.clone();
					e.getTracks().forEach((function(e, t) {
						var r = n.getTracks()[t];
						e.addEventListener("enabled", (function(e) {
							r.enabled = e.enabled
						}))
					})), n.getTracks().forEach((function(e) {
						r.addTrack(e, n)
					}))
				}
			}, i.prototype.removeTrack = function(t) {
				if (this._isClosed) throw pe("InvalidStateError",
					"Attempted to call removeTrack on a closed peerconnection.");
				if (!(t instanceof e.RTCRtpSender)) throw new TypeError(
					"Argument 1 of RTCPeerConnection.removeTrack does not implement interface RTCRtpSender."
					);
				var r = this.transceivers.find((function(e) {
					return e.rtpSender === t
				}));
				if (!r) throw pe("InvalidAccessError", "Sender was not created by this connection.");
				var n = r.stream;
				r.rtpSender.stop(), r.rtpSender = null, r.track = null, r.stream = null, -1 === this
					.transceivers.map((function(e) {
						return e.stream
					})).indexOf(n) && this.localStreams.indexOf(n) > -1 && this.localStreams.splice(this
						.localStreams.indexOf(n), 1), this._maybeFireNegotiationNeeded()
			}, i.prototype.removeStream = function(e) {
				var t = this;
				e.getTracks().forEach((function(e) {
					var r = t.getSenders().find((function(t) {
						return t.track === e
					}));
					r && t.removeTrack(r)
				}))
			}, i.prototype.getSenders = function() {
				return this.transceivers.filter((function(e) {
					return !!e.rtpSender
				})).map((function(e) {
					return e.rtpSender
				}))
			}, i.prototype.getReceivers = function() {
				return this.transceivers.filter((function(e) {
					return !!e.rtpReceiver
				})).map((function(e) {
					return e.rtpReceiver
				}))
			}, i.prototype._createIceGatherer = function(t, r) {
				var n = this;
				if (r && t > 0) return this.transceivers[0].iceGatherer;
				if (this._iceGatherers.length) return this._iceGatherers.shift();
				var i = new e.RTCIceGatherer({
					iceServers: this._config.iceServers,
					gatherPolicy: this._config.iceTransportPolicy
				});
				return Object.defineProperty(i, "state", {
						value: "new",
						writable: !0
					}), this.transceivers[t].bufferedCandidateEvents = [], this.transceivers[t]
					.bufferCandidates = function(e) {
						var r = !e.candidate || 0 === Object.keys(e.candidate).length;
						i.state = r ? "completed" : "gathering", null !== n.transceivers[t]
							.bufferedCandidateEvents && n.transceivers[t].bufferedCandidateEvents.push(e)
					}, i.addEventListener("localcandidate", this.transceivers[t].bufferCandidates), i
			}, i.prototype._gather = function(t, r) {
				var n = this,
					i = this.transceivers[r].iceGatherer;
				if (!i.onlocalcandidate) {
					var o = this.transceivers[r].bufferedCandidateEvents;
					this.transceivers[r].bufferedCandidateEvents = null, i.removeEventListener(
							"localcandidate", this.transceivers[r].bufferCandidates), i.onlocalcandidate =
						function(e) {
							if (!(n.usingBundle && r > 0)) {
								var o = new Event("icecandidate");
								o.candidate = {
									sdpMid: t,
									sdpMLineIndex: r
								};
								var s = e.candidate,
									a = !s || 0 === Object.keys(s).length;
								if (a) "new" !== i.state && "gathering" !== i.state || (i.state =
									"completed");
								else {
									"new" === i.state && (i.state = "gathering"), s.component = 1, s.ufrag =
										i.getLocalParameters().usernameFragment;
									var c = oe.writeCandidate(s);
									o.candidate = Object.assign(o.candidate, oe.parseCandidate(c)), o
										.candidate.candidate = c, o.candidate.toJSON = function() {
											return {
												candidate: o.candidate.candidate,
												sdpMid: o.candidate.sdpMid,
												sdpMLineIndex: o.candidate.sdpMLineIndex,
												usernameFragment: o.candidate.usernameFragment
											}
										}
								}
								var d = oe.getMediaSections(n._localDescription.sdp);
								d[o.candidate.sdpMLineIndex] += a ? "a=end-of-candidates\r\n" : "a=" + o
									.candidate.candidate + "\r\n", n._localDescription.sdp = oe
									.getDescription(n._localDescription.sdp) + d.join("");
								var p = n.transceivers.every((function(e) {
									return e.iceGatherer && "completed" === e.iceGatherer.state
								}));
								"gathering" !== n.iceGatheringState && (n.iceGatheringState = "gathering", n
									._emitGatheringStateChange()), a || n._dispatchEvent("icecandidate",
									o), p && (n._dispatchEvent("icecandidate", new Event(
										"icecandidate")), n.iceGatheringState = "complete", n
									._emitGatheringStateChange())
							}
						}, e.setTimeout((function() {
							o.forEach((function(e) {
								i.onlocalcandidate(e)
							}))
						}), 0)
				}
			}, i.prototype._createIceAndDtlsTransports = function() {
				var t = this,
					r = new e.RTCIceTransport(null);
				r.onicestatechange = function() {
					t._updateIceConnectionState(), t._updateConnectionState()
				};
				var n = new e.RTCDtlsTransport(r);
				return n.ondtlsstatechange = function() {
					t._updateConnectionState()
				}, n.onerror = function() {
					Object.defineProperty(n, "state", {
						value: "failed",
						writable: !0
					}), t._updateConnectionState()
				}, {
					iceTransport: r,
					dtlsTransport: n
				}
			}, i.prototype._disposeIceAndDtlsTransports = function(e) {
				var t = this.transceivers[e].iceGatherer;
				t && (delete t.onlocalcandidate, delete this.transceivers[e].iceGatherer);
				var r = this.transceivers[e].iceTransport;
				r && (delete r.onicestatechange, delete this.transceivers[e].iceTransport);
				var n = this.transceivers[e].dtlsTransport;
				n && (delete n.ondtlsstatechange, delete n.onerror, delete this.transceivers[e]
					.dtlsTransport)
			}, i.prototype._transceive = function(e, r, n) {
				var i = ae(e.localCapabilities, e.remoteCapabilities);
				r && e.rtpSender && (i.encodings = e.sendEncodingParameters, i.rtcp = {
					cname: oe.localCName,
					compound: e.rtcpParameters.compound
				}, e.recvEncodingParameters.length && (i.rtcp.ssrc = e.recvEncodingParameters[0]
					.ssrc), e.rtpSender.send(i)), n && e.rtpReceiver && i.codecs.length > 0 && (
					"video" === e.kind && e.recvEncodingParameters && t < 15019 && e
					.recvEncodingParameters.forEach((function(e) {
						delete e.rtx
					})), e.recvEncodingParameters.length ? i.encodings = e.recvEncodingParameters : i
					.encodings = [{}], i.rtcp = {
						compound: e.rtcpParameters.compound
					}, e.rtcpParameters.cname && (i.rtcp.cname = e.rtcpParameters.cname), e
					.sendEncodingParameters.length && (i.rtcp.ssrc = e.sendEncodingParameters[0].ssrc),
					e.rtpReceiver.receive(i))
			}, i.prototype.setLocalDescription = function(e) {
				var t, r, n = this;
				if (-1 === ["offer", "answer"].indexOf(e.type)) return Promise.reject(pe("TypeError",
					'Unsupported type "' + e.type + '"'));
				if (!ce("setLocalDescription", e.type, n.signalingState) || n._isClosed) return Promise
					.reject(pe("InvalidStateError", "Can not set local " + e.type + " in state " + n
						.signalingState));
				if ("offer" === e.type) t = oe.splitSections(e.sdp), r = t.shift(), t.forEach((function(e,
					t) {
					var r = oe.parseRtpParameters(e);
					n.transceivers[t].localCapabilities = r
				})), n.transceivers.forEach((function(e, t) {
					n._gather(e.mid, t)
				}));
				else if ("answer" === e.type) {
					t = oe.splitSections(n._remoteDescription.sdp), r = t.shift();
					var i = oe.matchPrefix(r, "a=ice-lite").length > 0;
					t.forEach((function(e, t) {
						var o = n.transceivers[t],
							s = o.iceGatherer,
							a = o.iceTransport,
							c = o.dtlsTransport,
							d = o.localCapabilities,
							p = o.remoteCapabilities;
						if (!(oe.isRejected(e) && 0 === oe.matchPrefix(e, "a=bundle-only")
								.length) && !o.rejected) {
							var l = oe.getIceParameters(e, r),
								u = oe.getDtlsParameters(e, r);
							i && (u.role = "server"), n.usingBundle && 0 !== t || (n._gather(o
									.mid, t), "new" === a.state && a.start(s, l, i ?
									"controlling" : "controlled"), "new" === c.state && c
								.start(u));
							var f = ae(d, p);
							n._transceive(o, f.codecs.length > 0, !1)
						}
					}))
				}
				return n._localDescription = {
						type: e.type,
						sdp: e.sdp
					}, "offer" === e.type ? n._updateSignalingState("have-local-offer") : n
					._updateSignalingState("stable"), Promise.resolve()
			}, i.prototype.setRemoteDescription = function(i) {
				var o = this;
				if (-1 === ["offer", "answer"].indexOf(i.type)) return Promise.reject(pe("TypeError",
					'Unsupported type "' + i.type + '"'));
				if (!ce("setRemoteDescription", i.type, o.signalingState) || o._isClosed) return Promise
					.reject(pe("InvalidStateError", "Can not set remote " + i.type + " in state " + o
						.signalingState));
				var s = {};
				o.remoteStreams.forEach((function(e) {
					s[e.id] = e
				}));
				var a = [],
					c = oe.splitSections(i.sdp),
					d = c.shift(),
					p = oe.matchPrefix(d, "a=ice-lite").length > 0,
					l = oe.matchPrefix(d, "a=group:BUNDLE ").length > 0;
				o.usingBundle = l;
				var u = oe.matchPrefix(d, "a=ice-options:")[0];
				return o.canTrickleIceCandidates = !!u && u.substr(14).split(" ").indexOf("trickle") >= 0, c
					.forEach((function(n, c) {
						var u = oe.splitLines(n),
							f = oe.getKind(n),
							h = oe.isRejected(n) && 0 === oe.matchPrefix(n, "a=bundle-only").length,
							m = u[0].substr(2).split(" ")[2],
							v = oe.getDirection(n, d),
							g = oe.parseMsid(n),
							y = oe.getMid(n) || oe.generateIdentifier();
						if (h || "application" === f && ("DTLS/SCTP" === m || "UDP/DTLS/SCTP" ===
							m)) o.transceivers[c] = {
							mid: y,
							kind: f,
							protocol: m,
							rejected: !0
						};
						else {
							var w, T, C, S, b, R, E, P, k;
							!h && o.transceivers[c] && o.transceivers[c].rejected && (o
								.transceivers[c] = o._createTransceiver(f, !0));
							var _, x, D = oe.parseRtpParameters(n);
							h || (_ = oe.getIceParameters(n, d), (x = oe.getDtlsParameters(n, d))
								.role = "client"), E = oe.parseRtpEncodingParameters(n);
							var O = oe.parseRtcpParameters(n),
								I = oe.matchPrefix(n, "a=end-of-candidates", d).length > 0,
								M = oe.matchPrefix(n, "a=candidate:").map((function(e) {
									return oe.parseCandidate(e)
								})).filter((function(e) {
									return 1 === e.component
								}));
							if (("offer" === i.type || "answer" === i.type) && !h && l && c > 0 && o
								.transceivers[c] && (o._disposeIceAndDtlsTransports(c), o
									.transceivers[c].iceGatherer = o.transceivers[0].iceGatherer, o
									.transceivers[c].iceTransport = o.transceivers[0].iceTransport,
									o.transceivers[c].dtlsTransport = o.transceivers[0]
									.dtlsTransport, o.transceivers[c].rtpSender && o.transceivers[c]
									.rtpSender.setTransport(o.transceivers[0].dtlsTransport), o
									.transceivers[c].rtpReceiver && o.transceivers[c].rtpReceiver
									.setTransport(o.transceivers[0].dtlsTransport)), "offer" !== i
								.type || h) {
								if ("answer" === i.type && !h) {
									T = (w = o.transceivers[c]).iceGatherer, C = w.iceTransport, S =
										w.dtlsTransport, b = w.rtpReceiver, R = w
										.sendEncodingParameters, P = w.localCapabilities, o
										.transceivers[c].recvEncodingParameters = E, o.transceivers[
											c].remoteCapabilities = D, o.transceivers[c]
										.rtcpParameters = O, M.length && "new" === C.state && (!p &&
											!I || l && 0 !== c ? M.forEach((function(e) {
												de(w.iceTransport, e)
											})) : C.setRemoteCandidates(M)), l && 0 !== c || (
											"new" === C.state && C.start(T, _, "controlling"),
											"new" === S.state && S.start(x)), !ae(w
											.localCapabilities, w.remoteCapabilities).codecs.filter(
											(function(e) {
												return "rtx" === e.name.toLowerCase()
											})).length && w.sendEncodingParameters[0].rtx &&
										delete w.sendEncodingParameters[0].rtx, o._transceive(w,
											"sendrecv" === v || "recvonly" === v, "sendrecv" ===
											v || "sendonly" === v), !b || "sendrecv" !== v &&
										"sendonly" !== v ? delete w.rtpReceiver : (k = b.track, g ?
											(s[g.stream] || (s[g.stream] = new e.MediaStream), r(k,
												s[g.stream]), a.push([k, b, s[g.stream]])) : (s
												.default || (s.default = new e.MediaStream), r(k, s
													.default), a.push([k, b, s.default])))
								}
							} else {
								(w = o.transceivers[c] || o._createTransceiver(f)).mid = y, w
									.iceGatherer || (w.iceGatherer = o._createIceGatherer(c, l)), M
									.length && "new" === w.iceTransport.state && (!I || l && 0 !==
										c ? M.forEach((function(e) {
											de(w.iceTransport, e)
										})) : w.iceTransport.setRemoteCandidates(M)), P = e
									.RTCRtpReceiver.getCapabilities(f), t < 15019 && (P.codecs = P
										.codecs.filter((function(e) {
											return "rtx" !== e.name
										}))), R = w.sendEncodingParameters || [{
										ssrc: 1001 * (2 * c + 2)
									}];
								var L, A = !1;
								if ("sendrecv" === v || "sendonly" === v) {
									if (A = !w.rtpReceiver, b = w.rtpReceiver || new e
										.RTCRtpReceiver(w.dtlsTransport, f), A) k = b.track, g &&
										"-" === g.stream || (g ? (s[g.stream] || (s[g.stream] =
											new e.MediaStream, Object.defineProperty(s[g
												.stream], "id", {
												get: function() {
													return g.stream
												}
											})), Object.defineProperty(k, "id", {
											get: function() {
												return g.track
											}
										}), L = s[g.stream]) : (s.default || (s.default = new e
											.MediaStream), L = s.default)), L && (r(k, L), w
											.associatedRemoteMediaStreams.push(L)), a.push([k, b,
											L])
								} else w.rtpReceiver && w.rtpReceiver.track && (w
									.associatedRemoteMediaStreams.forEach((function(t) {
										var r = t.getTracks().find((function(e) {
											return e.id === w.rtpReceiver
												.track.id
										}));
										r && function(t, r) {
											r.removeTrack(t), r.dispatchEvent(new e
												.MediaStreamTrackEvent(
													"removetrack", {
														track: t
													}))
										}(r, t)
									})), w.associatedRemoteMediaStreams = []);
								w.localCapabilities = P, w.remoteCapabilities = D, w.rtpReceiver =
									b, w.rtcpParameters = O, w.sendEncodingParameters = R, w
									.recvEncodingParameters = E, o._transceive(o.transceivers[c], !
										1, A)
							}
						}
					})), void 0 === o._dtlsRole && (o._dtlsRole = "offer" === i.type ? "active" :
					"passive"), o._remoteDescription = {
						type: i.type,
						sdp: i.sdp
					}, "offer" === i.type ? o._updateSignalingState("have-remote-offer") : o
					._updateSignalingState("stable"), Object.keys(s).forEach((function(t) {
						var r = s[t];
						if (r.getTracks().length) {
							if (-1 === o.remoteStreams.indexOf(r)) {
								o.remoteStreams.push(r);
								var i = new Event("addstream");
								i.stream = r, e.setTimeout((function() {
									o._dispatchEvent("addstream", i)
								}))
							}
							a.forEach((function(e) {
								var t = e[0],
									i = e[1];
								r.id === e[2].id && n(o, t, i, [r])
							}))
						}
					})), a.forEach((function(e) {
						e[2] || n(o, e[0], e[1], [])
					})), e.setTimeout((function() {
						o && o.transceivers && o.transceivers.forEach((function(e) {
							e.iceTransport && "new" === e.iceTransport.state && e
								.iceTransport.getRemoteCandidates().length > 0 && (
									console.warn(
										"Timeout for addRemoteCandidate. Consider sending an end-of-candidates notification"
										), e.iceTransport.addRemoteCandidate({}))
						}))
					}), 4e3), Promise.resolve()
			}, i.prototype.close = function() {
				this.transceivers.forEach((function(e) {
					e.iceTransport && e.iceTransport.stop(), e.dtlsTransport && e.dtlsTransport
						.stop(), e.rtpSender && e.rtpSender.stop(), e.rtpReceiver && e
						.rtpReceiver.stop()
				})), this._isClosed = !0, this._updateSignalingState("closed")
			}, i.prototype._updateSignalingState = function(e) {
				this.signalingState = e;
				var t = new Event("signalingstatechange");
				this._dispatchEvent("signalingstatechange", t)
			}, i.prototype._maybeFireNegotiationNeeded = function() {
				var t = this;
				"stable" === this.signalingState && !0 !== this.needNegotiation && (this.needNegotiation = !
					0, e.setTimeout((function() {
						if (t.needNegotiation) {
							t.needNegotiation = !1;
							var e = new Event("negotiationneeded");
							t._dispatchEvent("negotiationneeded", e)
						}
					}), 0))
			}, i.prototype._updateIceConnectionState = function() {
				var e, t = {
					new: 0,
					closed: 0,
					checking: 0,
					connected: 0,
					completed: 0,
					disconnected: 0,
					failed: 0
				};
				if (this.transceivers.forEach((function(e) {
						e.iceTransport && !e.rejected && t[e.iceTransport.state]++
					})), e = "new", t.failed > 0 ? e = "failed" : t.checking > 0 ? e = "checking" : t
					.disconnected > 0 ? e = "disconnected" : t.new > 0 ? e = "new" : t.connected > 0 ? e =
					"connected" : t.completed > 0 && (e = "completed"), e !== this.iceConnectionState) {
					this.iceConnectionState = e;
					var r = new Event("iceconnectionstatechange");
					this._dispatchEvent("iceconnectionstatechange", r)
				}
			}, i.prototype._updateConnectionState = function() {
				var e, t = {
					new: 0,
					closed: 0,
					connecting: 0,
					connected: 0,
					completed: 0,
					disconnected: 0,
					failed: 0
				};
				if (this.transceivers.forEach((function(e) {
						e.iceTransport && e.dtlsTransport && !e.rejected && (t[e.iceTransport
							.state]++, t[e.dtlsTransport.state]++)
					})), t.connected += t.completed, e = "new", t.failed > 0 ? e = "failed" : t.connecting >
					0 ? e = "connecting" : t.disconnected > 0 ? e = "disconnected" : t.new > 0 ? e = "new" :
					t.connected > 0 && (e = "connected"), e !== this.connectionState) {
					this.connectionState = e;
					var r = new Event("connectionstatechange");
					this._dispatchEvent("connectionstatechange", r)
				}
			}, i.prototype.createOffer = function() {
				var r = this;
				if (r._isClosed) return Promise.reject(pe("InvalidStateError",
					"Can not call createOffer after close"));
				var n = r.transceivers.filter((function(e) {
						return "audio" === e.kind
					})).length,
					i = r.transceivers.filter((function(e) {
						return "video" === e.kind
					})).length,
					o = arguments[0];
				if (o) {
					if (o.mandatory || o.optional) throw new TypeError(
						"Legacy mandatory/optional constraints not supported.");
					void 0 !== o.offerToReceiveAudio && (n = !0 === o.offerToReceiveAudio ? 1 : !1 === o
							.offerToReceiveAudio ? 0 : o.offerToReceiveAudio), void 0 !== o
						.offerToReceiveVideo && (i = !0 === o.offerToReceiveVideo ? 1 : !1 === o
							.offerToReceiveVideo ? 0 : o.offerToReceiveVideo)
				}
				for (r.transceivers.forEach((function(e) {
						"audio" === e.kind ? --n < 0 && (e.wantReceive = !1) : "video" === e.kind &&
							--i < 0 && (e.wantReceive = !1)
					})); n > 0 || i > 0;) n > 0 && (r._createTransceiver("audio"), n--), i > 0 && (r
					._createTransceiver("video"), i--);
				var s = oe.writeSessionBoilerplate(r._sdpSessionId, r._sdpSessionVersion++);
				r.transceivers.forEach((function(n, i) {
					var o = n.track,
						s = n.kind,
						a = n.mid || oe.generateIdentifier();
					n.mid = a, n.iceGatherer || (n.iceGatherer = r._createIceGatherer(i, r
						.usingBundle));
					var c = e.RTCRtpSender.getCapabilities(s);
					t < 15019 && (c.codecs = c.codecs.filter((function(e) {
						return "rtx" !== e.name
					}))), c.codecs.forEach((function(e) {
						"H264" === e.name && void 0 === e.parameters[
								"level-asymmetry-allowed"] && (e.parameters[
								"level-asymmetry-allowed"] = "1"), n
							.remoteCapabilities && n.remoteCapabilities.codecs && n
							.remoteCapabilities.codecs.forEach((function(t) {
								e.name.toLowerCase() === t.name
									.toLowerCase() && e.clockRate === t
									.clockRate && (e.preferredPayloadType =
										t.payloadType)
							}))
					})), c.headerExtensions.forEach((function(e) {
						(n.remoteCapabilities && n.remoteCapabilities
							.headerExtensions || []).forEach((function(t) {
							e.uri === t.uri && (e.id = t.id)
						}))
					}));
					var d = n.sendEncodingParameters || [{
						ssrc: 1001 * (2 * i + 1)
					}];
					o && t >= 15019 && "video" === s && !d[0].rtx && (d[0].rtx = {
							ssrc: d[0].ssrc + 1
						}), n.wantReceive && (n.rtpReceiver = new e.RTCRtpReceiver(n
							.dtlsTransport, s)), n.localCapabilities = c, n
						.sendEncodingParameters = d
				})), "max-compat" !== r._config.bundlePolicy && (s += "a=group:BUNDLE " + r.transceivers
					.map((function(e) {
						return e.mid
					})).join(" ") + "\r\n"), s += "a=ice-options:trickle\r\n", r.transceivers.forEach((
					function(e, t) {
						s += se(e, e.localCapabilities, "offer", e.stream, r._dtlsRole), s +=
							"a=rtcp-rsize\r\n", !e.iceGatherer || "new" === r.iceGatheringState ||
							0 !== t && r.usingBundle || (e.iceGatherer.getLocalCandidates().forEach(
								(function(e) {
									e.component = 1, s += "a=" + oe.writeCandidate(e) +
										"\r\n"
								})), "completed" === e.iceGatherer.state && (s +=
								"a=end-of-candidates\r\n"))
					}));
				var a = new e.RTCSessionDescription({
					type: "offer",
					sdp: s
				});
				return Promise.resolve(a)
			}, i.prototype.createAnswer = function() {
				var r = this;
				if (r._isClosed) return Promise.reject(pe("InvalidStateError",
					"Can not call createAnswer after close"));
				if ("have-remote-offer" !== r.signalingState && "have-local-pranswer" !== r.signalingState)
					return Promise.reject(pe("InvalidStateError",
						"Can not call createAnswer in signalingState " + r.signalingState));
				var n = oe.writeSessionBoilerplate(r._sdpSessionId, r._sdpSessionVersion++);
				r.usingBundle && (n += "a=group:BUNDLE " + r.transceivers.map((function(e) {
					return e.mid
				})).join(" ") + "\r\n"), n += "a=ice-options:trickle\r\n";
				var i = oe.getMediaSections(r._remoteDescription.sdp).length;
				r.transceivers.forEach((function(e, o) {
					if (!(o + 1 > i)) {
						if (e.rejected) return "application" === e.kind ? "DTLS/SCTP" === e
							.protocol ? n += "m=application 0 DTLS/SCTP 5000\r\n" : n +=
							"m=application 0 " + e.protocol + " webrtc-datachannel\r\n" :
							"audio" === e.kind ? n +=
							"m=audio 0 UDP/TLS/RTP/SAVPF 0\r\na=rtpmap:0 PCMU/8000\r\n" :
							"video" === e.kind && (n +=
								"m=video 0 UDP/TLS/RTP/SAVPF 120\r\na=rtpmap:120 VP8/90000\r\n"
								), void(n += "c=IN IP4 0.0.0.0\r\na=inactive\r\na=mid:" + e
								.mid + "\r\n");
						var s;
						if (e.stream) "audio" === e.kind ? s = e.stream.getAudioTracks()[0] :
							"video" === e.kind && (s = e.stream.getVideoTracks()[0]), s && t >=
							15019 && "video" === e.kind && !e.sendEncodingParameters[0].rtx && (
								e.sendEncodingParameters[0].rtx = {
									ssrc: e.sendEncodingParameters[0].ssrc + 1
								});
						var a = ae(e.localCapabilities, e.remoteCapabilities);
						!a.codecs.filter((function(e) {
								return "rtx" === e.name.toLowerCase()
							})).length && e.sendEncodingParameters[0].rtx && delete e
							.sendEncodingParameters[0].rtx, n += se(e, a, "answer", e.stream, r
								._dtlsRole), e.rtcpParameters && e.rtcpParameters.reducedSize &&
							(n += "a=rtcp-rsize\r\n")
					}
				}));
				var o = new e.RTCSessionDescription({
					type: "answer",
					sdp: n
				});
				return Promise.resolve(o)
			}, i.prototype.addIceCandidate = function(e) {
				var t, r = this;
				return e && void 0 === e.sdpMLineIndex && !e.sdpMid ? Promise.reject(new TypeError(
					"sdpMLineIndex or sdpMid required")) : new Promise((function(n, i) {
					if (!r._remoteDescription) return i(pe("InvalidStateError",
						"Can not add ICE candidate without a remote description"));
					if (e && "" !== e.candidate) {
						var o = e.sdpMLineIndex;
						if (e.sdpMid)
							for (var s = 0; s < r.transceivers.length; s++)
								if (r.transceivers[s].mid === e.sdpMid) {
									o = s;
									break
								} var a = r.transceivers[o];
						if (!a) return i(pe("OperationError", "Can not add ICE candidate"));
						if (a.rejected) return n();
						var c = Object.keys(e.candidate).length > 0 ? oe.parseCandidate(e
							.candidate) : {};
						if ("tcp" === c.protocol && (0 === c.port || 9 === c.port)) return n();
						if (c.component && 1 !== c.component) return n();
						if ((0 === o || o > 0 && a.iceTransport !== r.transceivers[0]
								.iceTransport) && !de(a.iceTransport, c)) return i(pe(
							"OperationError", "Can not add ICE candidate"));
						var d = e.candidate.trim();
						0 === d.indexOf("a=") && (d = d.substr(2)), (t = oe.getMediaSections(r
								._remoteDescription.sdp))[o] += "a=" + (c.type ? d :
								"end-of-candidates") + "\r\n", r._remoteDescription.sdp = oe
							.getDescription(r._remoteDescription.sdp) + t.join("")
					} else
						for (var p = 0; p < r.transceivers.length && (r.transceivers[p]
								.rejected || (r.transceivers[p].iceTransport
								.addRemoteCandidate({}), (t = oe.getMediaSections(r
										._remoteDescription.sdp))[p] +=
									"a=end-of-candidates\r\n", r._remoteDescription.sdp = oe
									.getDescription(r._remoteDescription.sdp) + t.join(""), !r
									.usingBundle)); p++);
					n()
				}))
			}, i.prototype.getStats = function(t) {
				if (t && t instanceof e.MediaStreamTrack) {
					var r = null;
					if (this.transceivers.forEach((function(e) {
							e.rtpSender && e.rtpSender.track === t ? r = e.rtpSender : e
								.rtpReceiver && e.rtpReceiver.track === t && (r = e.rtpReceiver)
						})), !r) throw pe("InvalidAccessError", "Invalid selector.");
					return r.getStats()
				}
				var n = [];
				return this.transceivers.forEach((function(e) {
					["rtpSender", "rtpReceiver", "iceGatherer", "iceTransport", "dtlsTransport"]
					.forEach((function(t) {
						e[t] && n.push(e[t].getStats())
					}))
				})), Promise.all(n).then((function(e) {
					var t = new Map;
					return e.forEach((function(e) {
						e.forEach((function(e) {
							t.set(e.id, e)
						}))
					})), t
				}))
			};
		["RTCRtpSender", "RTCRtpReceiver", "RTCIceGatherer", "RTCIceTransport", "RTCDtlsTransport"].forEach(
			(function(t) {
				var r = e[t];
				if (r && r.prototype && r.prototype.getStats) {
					var n = r.prototype.getStats;
					r.prototype.getStats = function() {
						return n.apply(this).then((function(e) {
							var t = new Map;
							return Object.keys(e).forEach((function(r) {
								var n;
								e[r].type = {
										inboundrtp: "inbound-rtp",
										outboundrtp: "outbound-rtp",
										candidatepair: "candidate-pair",
										localcandidate: "local-candidate",
										remotecandidate: "remote-candidate"
									} [(n = e[r]).type] || n.type, t
									.set(r, e[r])
							})), t
						}))
					}
				}
			}));
		var o = ["createOffer", "createAnswer"];
		return o.forEach((function(e) {
			var t = i.prototype[e];
			i.prototype[e] = function() {
				var e = arguments;
				return "function" == typeof e[0] || "function" == typeof e[1] ? t.apply(
					this, [arguments[2]]).then((function(t) {
					"function" == typeof e[0] && e[0].apply(null, [t])
				}), (function(t) {
					"function" == typeof e[1] && e[1].apply(null, [t])
				})) : t.apply(this, arguments)
			}
		})), (o = ["setLocalDescription", "setRemoteDescription", "addIceCandidate"]).forEach((function(
			e) {
			var t = i.prototype[e];
			i.prototype[e] = function() {
				var e = arguments;
				return "function" == typeof e[1] || "function" == typeof e[2] ? t.apply(
					this, arguments).then((function() {
					"function" == typeof e[1] && e[1].apply(null)
				}), (function(t) {
					"function" == typeof e[2] && e[2].apply(null, [t])
				})) : t.apply(this, arguments)
			}
		})), ["getStats"].forEach((function(e) {
			var t = i.prototype[e];
			i.prototype[e] = function() {
				var e = arguments;
				return "function" == typeof e[1] ? t.apply(this, arguments).then((
			function() {
					"function" == typeof e[1] && e[1].apply(null)
				})) : t.apply(this, arguments)
			}
		})), i
	};

	function ue(e) {
		const t = e && e.navigator,
			r = t.mediaDevices.getUserMedia.bind(t.mediaDevices);
		t.mediaDevices.getUserMedia = function(e) {
			return r(e).catch((e => Promise.reject(function(e) {
				return {
					name: {
						PermissionDeniedError: "NotAllowedError"
					} [e.name] || e.name,
					message: e.message,
					constraint: e.constraint,
					toString() {
						return this.name
					}
				}
			}(e))))
		}
	}

	function fe(e) {
		"getDisplayMedia" in e.navigator && e.navigator.mediaDevices && (e.navigator.mediaDevices &&
			"getDisplayMedia" in e.navigator.mediaDevices || (e.navigator.mediaDevices.getDisplayMedia = e
				.navigator.getDisplayMedia.bind(e.navigator)))
	}

	function he(e) {
		const t = V(e);
		if (e.RTCIceGatherer && (e.RTCIceCandidate || (e.RTCIceCandidate = function(e) {
				return e
			}), e.RTCSessionDescription || (e.RTCSessionDescription = function(e) {
				return e
			}), t.version < 15025)) {
			const t = Object.getOwnPropertyDescriptor(e.MediaStreamTrack.prototype, "enabled");
			Object.defineProperty(e.MediaStreamTrack.prototype, "enabled", {
				set(e) {
					t.set.call(this, e);
					const r = new Event("enabled");
					r.enabled = e, this.dispatchEvent(r)
				}
			})
		}
		e.RTCRtpSender && !("dtmf" in e.RTCRtpSender.prototype) && Object.defineProperty(e.RTCRtpSender
			.prototype, "dtmf", {
				get() {
					return void 0 === this._dtmf && ("audio" === this.track.kind ? this._dtmf = new e
							.RTCDtmfSender(this) : "video" === this.track.kind && (this._dtmf = null)),
						this._dtmf
				}
			}), e.RTCDtmfSender && !e.RTCDTMFSender && (e.RTCDTMFSender = e.RTCDtmfSender);
		const r = le(e, t.version);
		e.RTCPeerConnection = function(e) {
			return e && e.iceServers && (e.iceServers = function(e, t) {
				let r = !1;
				return (e = JSON.parse(JSON.stringify(e))).filter((e => {
					if (e && (e.urls || e.url)) {
						let t = e.urls || e.url;
						e.url && !e.urls && U("RTCIceServer.url", "RTCIceServer.urls");
						const n = "string" == typeof t;
						return n && (t = [t]), t = t.filter((e => {
							if (0 === e.indexOf("stun:")) return !1;
							const t = e.startsWith("turn") && !e.startsWith(
								"turn:[") && e.includes("transport=udp");
							return t && !r ? (r = !0, !0) : t && !r
						})), delete e.url, e.urls = n ? t[0] : t, !!t.length
					}
				}))
			}(e.iceServers, t.version), F("ICE servers after filtering:", e.iceServers)), new r(e)
		}, e.RTCPeerConnection.prototype = r.prototype
	}

	function me(e) {
		e.RTCRtpSender && !("replaceTrack" in e.RTCRtpSender.prototype) && (e.RTCRtpSender.prototype
			.replaceTrack = e.RTCRtpSender.prototype.setTrack)
	}
	var ve = Object.freeze({
		__proto__: null,
		shimPeerConnection: he,
		shimReplaceTrack: me,
		shimGetUserMedia: ue,
		shimGetDisplayMedia: fe
	});

	function ge(e) {
		const t = V(e),
			r = e && e.navigator,
			n = e && e.MediaStreamTrack;
		if (r.getUserMedia = function(e, t, n) {
				U("navigator.getUserMedia", "navigator.mediaDevices.getUserMedia"), r.mediaDevices.getUserMedia(
					e).then(t, n)
			}, !(t.version > 55 && "autoGainControl" in r.mediaDevices.getSupportedConstraints())) {
			const e = function(e, t, r) {
					t in e && !(r in e) && (e[r] = e[t], delete e[t])
				},
				t = r.mediaDevices.getUserMedia.bind(r.mediaDevices);
			if (r.mediaDevices.getUserMedia = function(r) {
					return "object" == typeof r && "object" == typeof r.audio && (r = JSON.parse(JSON.stringify(
						r)), e(r.audio, "autoGainControl", "mozAutoGainControl"), e(r.audio,
						"noiseSuppression", "mozNoiseSuppression")), t(r)
				}, n && n.prototype.getSettings) {
				const t = n.prototype.getSettings;
				n.prototype.getSettings = function() {
					const r = t.apply(this, arguments);
					return e(r, "mozAutoGainControl", "autoGainControl"), e(r, "mozNoiseSuppression",
						"noiseSuppression"), r
				}
			}
			if (n && n.prototype.applyConstraints) {
				const t = n.prototype.applyConstraints;
				n.prototype.applyConstraints = function(r) {
					return "audio" === this.kind && "object" == typeof r && (r = JSON.parse(JSON.stringify(
						r)), e(r, "autoGainControl", "mozAutoGainControl"), e(r, "noiseSuppression",
						"mozNoiseSuppression")), t.apply(this, [r])
				}
			}
		}
	}

	function ye(e) {
		"object" == typeof e && e.RTCTrackEvent && "receiver" in e.RTCTrackEvent.prototype && !("transceiver" in
			e.RTCTrackEvent.prototype) && Object.defineProperty(e.RTCTrackEvent.prototype, "transceiver", {
			get() {
				return {
					receiver: this.receiver
				}
			}
		})
	}

	function we(e) {
		const t = V(e);
		if ("object" != typeof e || !e.RTCPeerConnection && !e.mozRTCPeerConnection) return;
		if (!e.RTCPeerConnection && e.mozRTCPeerConnection && (e.RTCPeerConnection = e.mozRTCPeerConnection), t
			.version < 53 && ["setLocalDescription", "setRemoteDescription", "addIceCandidate"].forEach((
				function(t) {
					const r = e.RTCPeerConnection.prototype[t],
						n = {
							[t]() {
								return arguments[0] = new("addIceCandidate" === t ? e.RTCIceCandidate : e
									.RTCSessionDescription)(arguments[0]), r.apply(this, arguments)
							}
						};
					e.RTCPeerConnection.prototype[t] = n[t]
				})), t.version < 68) {
			const t = e.RTCPeerConnection.prototype.addIceCandidate;
			e.RTCPeerConnection.prototype.addIceCandidate = function() {
				return arguments[0] ? arguments[0] && "" === arguments[0].candidate ? Promise.resolve() : t
					.apply(this, arguments) : (arguments[1] && arguments[1].apply(null), Promise.resolve())
			}
		}
		const r = {
				inboundrtp: "inbound-rtp",
				outboundrtp: "outbound-rtp",
				candidatepair: "candidate-pair",
				localcandidate: "local-candidate",
				remotecandidate: "remote-candidate"
			},
			n = e.RTCPeerConnection.prototype.getStats;
		e.RTCPeerConnection.prototype.getStats = function() {
			const [e, i, o] = arguments;
			return n.apply(this, [e || null]).then((e => {
				if (t.version < 53 && !i) try {
					e.forEach((e => {
						e.type = r[e.type] || e.type
					}))
				} catch (t) {
					if ("TypeError" !== t.name) throw t;
					e.forEach(((t, n) => {
						e.set(n, Object.assign({}, t, {
							type: r[t.type] || t.type
						}))
					}))
				}
				return e
			})).then(i, o)
		}
	}

	function Te(e) {
		if ("object" != typeof e || !e.RTCPeerConnection || !e.RTCRtpSender) return;
		if (e.RTCRtpSender && "getStats" in e.RTCRtpSender.prototype) return;
		const t = e.RTCPeerConnection.prototype.getSenders;
		t && (e.RTCPeerConnection.prototype.getSenders = function() {
			const e = t.apply(this, []);
			return e.forEach((e => e._pc = this)), e
		});
		const r = e.RTCPeerConnection.prototype.addTrack;
		r && (e.RTCPeerConnection.prototype.addTrack = function() {
			const e = r.apply(this, arguments);
			return e._pc = this, e
		}), e.RTCRtpSender.prototype.getStats = function() {
			return this.track ? this._pc.getStats(this.track) : Promise.resolve(new Map)
		}
	}

	function Ce(e) {
		if ("object" != typeof e || !e.RTCPeerConnection || !e.RTCRtpSender) return;
		if (e.RTCRtpSender && "getStats" in e.RTCRtpReceiver.prototype) return;
		const t = e.RTCPeerConnection.prototype.getReceivers;
		t && (e.RTCPeerConnection.prototype.getReceivers = function() {
				const e = t.apply(this, []);
				return e.forEach((e => e._pc = this)), e
			}), N(e, "track", (e => (e.receiver._pc = e.srcElement, e))), e.RTCRtpReceiver.prototype.getStats =
			function() {
				return this._pc.getStats(this.track)
			}
	}

	function Se(e) {
		e.RTCPeerConnection && !("removeStream" in e.RTCPeerConnection.prototype) && (e.RTCPeerConnection
			.prototype.removeStream = function(e) {
				U("removeStream", "removeTrack"), this.getSenders().forEach((t => {
					t.track && e.getTracks().includes(t.track) && this.removeTrack(t)
				}))
			})
	}

	function be(e) {
		e.DataChannel && !e.RTCDataChannel && (e.RTCDataChannel = e.DataChannel)
	}

	function Re(e) {
		if ("object" != typeof e || !e.RTCPeerConnection) return;
		const t = e.RTCPeerConnection.prototype.addTransceiver;
		t && (e.RTCPeerConnection.prototype.addTransceiver = function() {
			this.setParametersPromises = [];
			const e = arguments[1],
				r = e && "sendEncodings" in e;
			r && e.sendEncodings.forEach((e => {
				if ("rid" in e) {
					if (!/^[a-z0-9]{0,16}$/i.test(e.rid)) throw new TypeError(
						"Invalid RID value provided.")
				}
				if ("scaleResolutionDownBy" in e && !(parseFloat(e.scaleResolutionDownBy) >=
						1)) throw new RangeError("scale_resolution_down_by must be >= 1.0");
				if ("maxFramerate" in e && !(parseFloat(e.maxFramerate) >= 0))
				throw new RangeError("max_framerate must be >= 0.0")
			}));
			const n = t.apply(this, arguments);
			if (r) {
				const {
					sender: t
				} = n, r = t.getParameters();
				(!("encodings" in r) || 1 === r.encodings.length && 0 === Object.keys(r.encodings[0])
					.length) && (r.encodings = e.sendEncodings, t.sendEncodings = e.sendEncodings, this
					.setParametersPromises.push(t.setParameters(r).then((() => {
						delete t.sendEncodings
					})).catch((() => {
						delete t.sendEncodings
					}))))
			}
			return n
		})
	}

	function Ee(e) {
		if ("object" != typeof e || !e.RTCRtpSender) return;
		const t = e.RTCRtpSender.prototype.getParameters;
		t && (e.RTCRtpSender.prototype.getParameters = function() {
			const e = t.apply(this, arguments);
			return "encodings" in e || (e.encodings = [].concat(this.sendEncodings || [{}])), e
		})
	}

	function Pe(e) {
		if ("object" != typeof e || !e.RTCPeerConnection) return;
		const t = e.RTCPeerConnection.prototype.createOffer;
		e.RTCPeerConnection.prototype.createOffer = function() {
			return this.setParametersPromises && this.setParametersPromises.length ? Promise.all(this
				.setParametersPromises).then((() => t.apply(this, arguments))).finally((() => {
				this.setParametersPromises = []
			})) : t.apply(this, arguments)
		}
	}

	function ke(e) {
		if ("object" != typeof e || !e.RTCPeerConnection) return;
		const t = e.RTCPeerConnection.prototype.createAnswer;
		e.RTCPeerConnection.prototype.createAnswer = function() {
			return this.setParametersPromises && this.setParametersPromises.length ? Promise.all(this
				.setParametersPromises).then((() => t.apply(this, arguments))).finally((() => {
				this.setParametersPromises = []
			})) : t.apply(this, arguments)
		}
	}
	var _e = Object.freeze({
		__proto__: null,
		shimOnTrack: ye,
		shimPeerConnection: we,
		shimSenderGetStats: Te,
		shimReceiverGetStats: Ce,
		shimRemoveStream: Se,
		shimRTCDataChannel: be,
		shimAddTransceiver: Re,
		shimGetParameters: Ee,
		shimCreateOffer: Pe,
		shimCreateAnswer: ke,
		shimGetUserMedia: ge,
		shimGetDisplayMedia: function(e, t) {
			e.navigator.mediaDevices && "getDisplayMedia" in e.navigator.mediaDevices || e.navigator
				.mediaDevices && (e.navigator.mediaDevices.getDisplayMedia = function(r) {
					if (!r || !r.video) {
						const e = new DOMException(
							"getDisplayMedia without video constraints is undefined");
						return e.name = "NotFoundError", e.code = 8, Promise.reject(e)
					}
					return !0 === r.video ? r.video = {
						mediaSource: t
					} : r.video.mediaSource = t, e.navigator.mediaDevices.getUserMedia(r)
				})
		}
	});

	function xe(e) {
		if ("object" == typeof e && e.RTCPeerConnection) {
			if ("getLocalStreams" in e.RTCPeerConnection.prototype || (e.RTCPeerConnection.prototype
					.getLocalStreams = function() {
						return this._localStreams || (this._localStreams = []), this._localStreams
					}), !("addStream" in e.RTCPeerConnection.prototype)) {
				const t = e.RTCPeerConnection.prototype.addTrack;
				e.RTCPeerConnection.prototype.addStream = function(e) {
					this._localStreams || (this._localStreams = []), this._localStreams.includes(e) || this
						._localStreams.push(e), e.getAudioTracks().forEach((r => t.call(this, r, e))), e
						.getVideoTracks().forEach((r => t.call(this, r, e)))
				}, e.RTCPeerConnection.prototype.addTrack = function(e, ...r) {
					return r && r.forEach((e => {
						this._localStreams ? this._localStreams.includes(e) || this
							._localStreams.push(e) : this._localStreams = [e]
					})), t.apply(this, arguments)
				}
			}
			"removeStream" in e.RTCPeerConnection.prototype || (e.RTCPeerConnection.prototype.removeStream =
				function(e) {
					this._localStreams || (this._localStreams = []);
					const t = this._localStreams.indexOf(e);
					if (-1 === t) return;
					this._localStreams.splice(t, 1);
					const r = e.getTracks();
					this.getSenders().forEach((e => {
						r.includes(e.track) && this.removeTrack(e)
					}))
				})
		}
	}

	function De(e) {
		if ("object" == typeof e && e.RTCPeerConnection && ("getRemoteStreams" in e.RTCPeerConnection
				.prototype || (e.RTCPeerConnection.prototype.getRemoteStreams = function() {
					return this._remoteStreams ? this._remoteStreams : []
				}), !("onaddstream" in e.RTCPeerConnection.prototype))) {
			Object.defineProperty(e.RTCPeerConnection.prototype, "onaddstream", {
				get() {
					return this._onaddstream
				},
				set(e) {
					this._onaddstream && (this.removeEventListener("addstream", this._onaddstream),
							this.removeEventListener("track", this._onaddstreampoly)), this
						.addEventListener("addstream", this._onaddstream = e), this
						.addEventListener("track", this._onaddstreampoly = e => {
							e.streams.forEach((e => {
								if (this._remoteStreams || (this
									._remoteStreams = []), this._remoteStreams
									.includes(e)) return;
								this._remoteStreams.push(e);
								const t = new Event("addstream");
								t.stream = e, this.dispatchEvent(t)
							}))
						})
				}
			});
			const t = e.RTCPeerConnection.prototype.setRemoteDescription;
			e.RTCPeerConnection.prototype.setRemoteDescription = function() {
				const e = this;
				return this._onaddstreampoly || this.addEventListener("track", this._onaddstreampoly =
					function(t) {
						t.streams.forEach((t => {
							if (e._remoteStreams || (e._remoteStreams = []), e
								._remoteStreams.indexOf(t) >= 0) return;
							e._remoteStreams.push(t);
							const r = new Event("addstream");
							r.stream = t, e.dispatchEvent(r)
						}))
					}), t.apply(e, arguments)
			}
		}
	}

	function Oe(e) {
		if ("object" != typeof e || !e.RTCPeerConnection) return;
		const t = e.RTCPeerConnection.prototype,
			r = t.createOffer,
			n = t.createAnswer,
			i = t.setLocalDescription,
			o = t.setRemoteDescription,
			s = t.addIceCandidate;
		t.createOffer = function(e, t) {
			const n = arguments.length >= 2 ? arguments[2] : arguments[0],
				i = r.apply(this, [n]);
			return t ? (i.then(e, t), Promise.resolve()) : i
		}, t.createAnswer = function(e, t) {
			const r = arguments.length >= 2 ? arguments[2] : arguments[0],
				i = n.apply(this, [r]);
			return t ? (i.then(e, t), Promise.resolve()) : i
		};
		let a = function(e, t, r) {
			const n = i.apply(this, [e]);
			return r ? (n.then(t, r), Promise.resolve()) : n
		};
		t.setLocalDescription = a, a = function(e, t, r) {
			const n = o.apply(this, [e]);
			return r ? (n.then(t, r), Promise.resolve()) : n
		}, t.setRemoteDescription = a, a = function(e, t, r) {
			const n = s.apply(this, [e]);
			return r ? (n.then(t, r), Promise.resolve()) : n
		}, t.addIceCandidate = a
	}

	function Ie(e) {
		const t = e && e.navigator;
		if (t.mediaDevices && t.mediaDevices.getUserMedia) {
			const e = t.mediaDevices,
				r = e.getUserMedia.bind(e);
			t.mediaDevices.getUserMedia = e => r(Me(e))
		}!t.getUserMedia && t.mediaDevices && t.mediaDevices.getUserMedia && (t.getUserMedia = function(e, r,
		n) {
			t.mediaDevices.getUserMedia(e).then(r, n)
		}.bind(t))
	}

	function Me(e) {
		return e && void 0 !== e.video ? Object.assign({}, e, {
			video: J(e.video)
		}) : e
	}

	function Le(e) {
		if (!e.RTCPeerConnection) return;
		const t = e.RTCPeerConnection;
		e.RTCPeerConnection = function(e, r) {
			if (e && e.iceServers) {
				const t = [];
				for (let r = 0; r < e.iceServers.length; r++) {
					let n = e.iceServers[r];
					!n.hasOwnProperty("urls") && n.hasOwnProperty("url") ? (U("RTCIceServer.url",
							"RTCIceServer.urls"), n = JSON.parse(JSON.stringify(n)), n.urls = n.url,
						delete n.url, t.push(n)) : t.push(e.iceServers[r])
				}
				e.iceServers = t
			}
			return new t(e, r)
		}, e.RTCPeerConnection.prototype = t.prototype, "generateCertificate" in t && Object.defineProperty(
			e.RTCPeerConnection, "generateCertificate", {
				get: () => t.generateCertificate
			})
	}

	function Ae(e) {
		"object" == typeof e && e.RTCTrackEvent && "receiver" in e.RTCTrackEvent.prototype && !("transceiver" in
			e.RTCTrackEvent.prototype) && Object.defineProperty(e.RTCTrackEvent.prototype, "transceiver", {
			get() {
				return {
					receiver: this.receiver
				}
			}
		})
	}

	function je(e) {
		const t = e.RTCPeerConnection.prototype.createOffer;
		e.RTCPeerConnection.prototype.createOffer = function(e) {
			if (e) {
				void 0 !== e.offerToReceiveAudio && (e.offerToReceiveAudio = !!e.offerToReceiveAudio);
				const t = this.getTransceivers().find((e => "audio" === e.receiver.track.kind));
				!1 === e.offerToReceiveAudio && t ? "sendrecv" === t.direction ? t.setDirection ? t
					.setDirection("sendonly") : t.direction = "sendonly" : "recvonly" === t.direction && (t
						.setDirection ? t.setDirection("inactive") : t.direction = "inactive") : !0 !== e
					.offerToReceiveAudio || t || this.addTransceiver("audio"), void 0 !== e
					.offerToReceiveVideo && (e.offerToReceiveVideo = !!e.offerToReceiveVideo);
				const r = this.getTransceivers().find((e => "video" === e.receiver.track.kind));
				!1 === e.offerToReceiveVideo && r ? "sendrecv" === r.direction ? r.setDirection ? r
					.setDirection("sendonly") : r.direction = "sendonly" : "recvonly" === r.direction && (r
						.setDirection ? r.setDirection("inactive") : r.direction = "inactive") : !0 !== e
					.offerToReceiveVideo || r || this.addTransceiver("video")
			}
			return t.apply(this, arguments)
		}
	}

	function Ne(e) {
		"object" != typeof e || e.AudioContext || (e.AudioContext = e.webkitAudioContext)
	}
	var ze = Object.freeze({
		__proto__: null,
		shimLocalStreamsAPI: xe,
		shimRemoteStreamsAPI: De,
		shimCallbacksAPI: Oe,
		shimGetUserMedia: Ie,
		shimConstraints: Me,
		shimRTCIceServerUrls: Le,
		shimTrackEventTransceiver: Ae,
		shimCreateOfferLegacy: je,
		shimAudioContext: Ne
	});

	function Ge(e) {
		if (!e.RTCIceCandidate || e.RTCIceCandidate && "foundation" in e.RTCIceCandidate.prototype) return;
		const t = e.RTCIceCandidate;
		e.RTCIceCandidate = function(e) {
			if ("object" == typeof e && e.candidate && 0 === e.candidate.indexOf("a=") && ((e = JSON.parse(
					JSON.stringify(e))).candidate = e.candidate.substr(2)), e.candidate && e.candidate
				.length) {
				const r = new t(e),
					n = oe.parseCandidate(e.candidate),
					i = Object.assign(r, n);
				return i.toJSON = function() {
					return {
						candidate: i.candidate,
						sdpMid: i.sdpMid,
						sdpMLineIndex: i.sdpMLineIndex,
						usernameFragment: i.usernameFragment
					}
				}, i
			}
			return new t(e)
		}, e.RTCIceCandidate.prototype = t.prototype, N(e, "icecandidate", (t => (t.candidate && Object
			.defineProperty(t, "candidate", {
				value: new e.RTCIceCandidate(t.candidate),
				writable: "false"
			}), t)))
	}

	function Fe(e) {
		if (!e.RTCPeerConnection) return;
		const t = V(e);
		"sctp" in e.RTCPeerConnection.prototype || Object.defineProperty(e.RTCPeerConnection.prototype,
		"sctp", {
			get() {
				return void 0 === this._sctp ? null : this._sctp
			}
		});
		const r = function(e) {
				if (!e || !e.sdp) return !1;
				const t = oe.splitSections(e.sdp);
				return t.shift(), t.some((e => {
					const t = oe.parseMLine(e);
					return t && "application" === t.kind && -1 !== t.protocol.indexOf("SCTP")
				}))
			},
			n = function(e) {
				const t = e.sdp.match(/mozilla...THIS_IS_SDPARTA-(\d+)/);
				if (null === t || t.length < 2) return -1;
				const r = parseInt(t[1], 10);
				return r != r ? -1 : r
			},
			i = function(e) {
				let r = 65536;
				return "firefox" === t.browser && (r = t.version < 57 ? -1 === e ? 16384 : 2147483637 : t
					.version < 60 ? 57 === t.version ? 65535 : 65536 : 2147483637), r
			},
			o = function(e, r) {
				let n = 65536;
				"firefox" === t.browser && 57 === t.version && (n = 65535);
				const i = oe.matchPrefix(e.sdp, "a=max-message-size:");
				return i.length > 0 ? n = parseInt(i[0].substr(19), 10) : "firefox" === t.browser && -1 !== r &&
					(n = 2147483637), n
			},
			s = e.RTCPeerConnection.prototype.setRemoteDescription;
		e.RTCPeerConnection.prototype.setRemoteDescription = function() {
			if (this._sctp = null, "chrome" === t.browser && t.version >= 76) {
				const {
					sdpSemantics: e
				} = this.getConfiguration();
				"plan-b" === e && Object.defineProperty(this, "sctp", {
					get() {
						return void 0 === this._sctp ? null : this._sctp
					},
					enumerable: !0,
					configurable: !0
				})
			}
			if (r(arguments[0])) {
				const e = n(arguments[0]),
					t = i(e),
					r = o(arguments[0], e);
				let s;
				s = 0 === t && 0 === r ? Number.POSITIVE_INFINITY : 0 === t || 0 === r ? Math.max(t, r) :
					Math.min(t, r);
				const a = {};
				Object.defineProperty(a, "maxMessageSize", {
					get: () => s
				}), this._sctp = a
			}
			return s.apply(this, arguments)
		}
	}

	function Ue(e) {
		if (!e.RTCPeerConnection || !("createDataChannel" in e.RTCPeerConnection.prototype)) return;

		function t(e, t) {
			const r = e.send;
			e.send = function() {
				const n = arguments[0],
					i = n.length || n.size || n.byteLength;
				if ("open" === e.readyState && t.sctp && i > t.sctp.maxMessageSize) throw new TypeError(
					"Message too large (can send a maximum of " + t.sctp.maxMessageSize + " bytes)");
				return r.apply(e, arguments)
			}
		}
		const r = e.RTCPeerConnection.prototype.createDataChannel;
		e.RTCPeerConnection.prototype.createDataChannel = function() {
			const e = r.apply(this, arguments);
			return t(e, this), e
		}, N(e, "datachannel", (e => (t(e.channel, e.target), e)))
	}

	function Ve(e) {
		if (!e.RTCPeerConnection || "connectionState" in e.RTCPeerConnection.prototype) return;
		const t = e.RTCPeerConnection.prototype;
		Object.defineProperty(t, "connectionState", {
			get() {
				return {
					completed: "connected",
					checking: "connecting"
				} [this.iceConnectionState] || this.iceConnectionState
			},
			enumerable: !0,
			configurable: !0
		}), Object.defineProperty(t, "onconnectionstatechange", {
			get() {
				return this._onconnectionstatechange || null
			},
			set(e) {
				this._onconnectionstatechange && (this.removeEventListener("connectionstatechange",
						this._onconnectionstatechange), delete this._onconnectionstatechange), e &&
					this.addEventListener("connectionstatechange", this._onconnectionstatechange =
						e)
			},
			enumerable: !0,
			configurable: !0
		}), ["setLocalDescription", "setRemoteDescription"].forEach((e => {
			const r = t[e];
			t[e] = function() {
				return this._connectionstatechangepoly || (this._connectionstatechangepoly =
					e => {
						const t = e.target;
						if (t._lastConnectionState !== t.connectionState) {
							t._lastConnectionState = t.connectionState;
							const r = new Event("connectionstatechange", e);
							t.dispatchEvent(r)
						}
						return e
					}, this.addEventListener("iceconnectionstatechange", this
						._connectionstatechangepoly)), r.apply(this, arguments)
			}
		}))
	}

	function Be(e) {
		if (!e.RTCPeerConnection) return;
		const t = V(e);
		if ("chrome" === t.browser && t.version >= 71) return;
		if ("safari" === t.browser && t.version >= 605) return;
		const r = e.RTCPeerConnection.prototype.setRemoteDescription;
		e.RTCPeerConnection.prototype.setRemoteDescription = function(e) {
			return e && e.sdp && -1 !== e.sdp.indexOf("\na=extmap-allow-mixed") && (e.sdp = e.sdp.split(
				"\n").filter((e => "a=extmap-allow-mixed" !== e.trim())).join("\n")), r.apply(this,
				arguments)
		}
	}
	var Je = Object.freeze({
		__proto__: null,
		shimRTCIceCandidate: Ge,
		shimMaxMessageSize: Fe,
		shimSendThrowTypeError: Ue,
		shimConnectionState: Ve,
		removeAllowExtmapMixed: Be
	});
	const qe = function({
		window: e
	} = {}, t = {
		shimChrome: !0,
		shimFirefox: !0,
		shimEdge: !0,
		shimSafari: !0
	}) {
		const r = F,
			n = V(e),
			i = {
				browserDetails: n,
				commonShim: Je,
				extractVersion: j,
				disableLog: z,
				disableWarnings: G
			};
		switch (n.browser) {
			case "chrome":
				if (!ie || !re || !t.shimChrome) return r(
					"Chrome shim is not included in this adapter release."), i;
				if (null === n.version) return r("Chrome shim can not determine version, not shimming."), i;
				r("adapter.js shimming chrome."), i.browserShim = ie, Y(e), K(e), re(e), Q(e), te(e), $(e),
					X(e), Z(e), ne(e), Ge(e), Ve(e), Fe(e), Ue(e), Be(e);
				break;
			case "firefox":
				if (!_e || !we || !t.shimFirefox) return r(
					"Firefox shim is not included in this adapter release."), i;
				r("adapter.js shimming firefox."), i.browserShim = _e, ge(e), we(e), ye(e), Se(e), Te(e),
					Ce(e), be(e), Re(e), Ee(e), Pe(e), ke(e), Ge(e), Ve(e), Fe(e), Ue(e);
				break;
			case "edge":
				if (!ve || !he || !t.shimEdge) return r(
					"MS edge shim is not included in this adapter release."), i;
				r("adapter.js shimming edge."), i.browserShim = ve, ue(e), fe(e), he(e), me(e), Fe(e), Ue(
				e);
				break;
			case "safari":
				if (!ze || !t.shimSafari) return r("Safari shim is not included in this adapter release."),
					i;
				r("adapter.js shimming safari."), i.browserShim = ze, Le(e), je(e), Oe(e), xe(e), De(e), Ae(
					e), Ie(e), Ne(e), Ge(e), Fe(e), Ue(e), Be(e);
				break;
			default:
				r("Unsupported browser!")
		}
		return i
	}({
		window: "undefined" == typeof window ? void 0 : window
	});
	qe.browserDetails.browser, qe.browserDetails.version, qe.browserDetails.supportsUnifiedPlan;
	var We = function() {
			function e() {
				this.statsIntervalTime = 1e3, this.statsReportSleepTime = 2e3
			}
			return e.prototype.initPc = function() {
				this.release();
				var e = new RTCPeerConnection;
				e.onnegotiationneeded = function() {
					h.log("pc.onnegotiationneeded")
				}, e.onicecandidate = function(e) {
					h.log("pc.onicecandidate: " + g(e.candidate))
				}, e.oniceconnectionstatechange = function() {
					h.log("pc.oniceconnectionstatechange: " + e.iceConnectionState)
				}, e.onicegatheringstatechange = function() {
					h.log("pc.onicegatheringstatechange : " + e.iceGatheringState)
				}, e.onsignalingstatechange = function() {
					h.log("pc.onsignalingstatechange: " + e.signalingState)
				}, this.pc = e
			}, e.prototype.pullStream = function(e) {
				var t = this;
				return this.initPc(), new Promise((function(r, s) {
					return i(t, void 0, void 0, (function() {
						var t, i, a, c, d, p, f, m = this;
						return o(this, (function(o) {
							switch (o.label) {
								case 0:
									return o.trys.push([0, 5, , 6]), t =
										new MediaStream, this.pc
										.onconnectionstatechange =
										function() {
											switch (h.log(
													"pc.onconnectionstatechange: " +
													m.pc.connectionState
													), m.pc
												.connectionState) {
												case "connected":
													m.initStats(), r(t);
													break;
												case "disconnected":
													e = {
														code: 20006,
														errorType: "connectFailed",
														msg: "pc connection disconnected"
													}, P.emit(
														"error", e);
												case "failed":
												case "closed":
													s(new T("peerconnection connect error: " +
														m.pc
														.connectionState
														))
											}
											var e
										}, this.pc.ontrack = function(
										e) {
											h.log("peerConnection.ontrack, kind: " +
													e.track.kind +
													" + ', id: " + e
													.track.id),
												"audio" === e.track
												.kind && (m.audioTrack =
													e.track),
												"video" === e.track
												.kind && (m.videoTrack =
													e.track), t
												.addTrack(e.track)
										}, i = g(n(n({}, l), {
											SDK_VERSION: R
										})), [4, this.createOffer()];
								case 1:
									return a = o.sent(), h.log(
											"local offer: \n" + a.sdp),
										a = this.mungSDP(a), [4, this
											.setLocal(a)
										];
								case 2:
									if (o.sent(), !(c =
											/[a-zA-Z0-9]{3,7}:\/\/([^/]+)\//
											.exec(e))) throw new T(
										"streamurl is not valid: " +
										e);
									return [4, u(location.protocol +
										"//" + c[1] +
										"/rtc/v1/play", {
											streamurl: e,
											clientip: i,
											sdp: a.sdp
										})];
								case 3:
									return d = o.sent(), h.log(
											"remote answer, \n" + d.sdp
											), this.sessionId = d
										.sessionid, p =
										new RTCSessionDescription({
											type: "answer",
											sdp: d.sdp
										}), [4, this.setRemote(p)];
								case 4:
									return o.sent(), [3, 6];
								case 5:
									return f = o.sent(), s(
										f instanceof Error ? new T(f
											.message) : new T(
											String(f))), [3, 6];
								case 6:
									return [2]
							}
						}))
					}))
				}))
			}, e.prototype.getSessionId = function() {
				return this.sessionId
			}, e.prototype.initStats = function() {
				var e = this;
				this.statsIntervalId && clearInterval(this.statsIntervalId), this.statsIntervalId =
					setInterval((function() {
						var t, r;
						e.pc.getStats().then((function(e) {
							t = e
						})).then((function() {
							return new Promise((function(t) {
								setTimeout(t, e.statsReportSleepTime)
							}))
						})).then((function() {
							return e.pc.getStats()
						})).then((function(n) {
							r = n;
							var i, o = e.processStats(t, r);
							i = o, P.emit("stats", i), h.log("stats: " + g(o))
						})).catch((function(e) {
							h.debug("getStats error: " + e.toString())
						}))
					}), this.statsIntervalTime)
			}, e.prototype.release = function() {
				this.pc && this.pc.close(), this.statsIntervalId && clearInterval(this.statsIntervalId)
			}, e.prototype.processStats = function(e, t) {
				var r = this,
					n = S;
				return t.forEach((function(t) {
					if ("inbound-rtp" === t.type && !0 !== t.isRemote) {
						if ("audio" === t.mediaType || t.id.toLocaleLowerCase().includes(
								"audio")) {
							if (!(i = e.get(t.id))) return;
							n.audioBitrate = y(8 * (t.bytesReceived - i.bytesReceived) / 1e3 / (
								r.statsReportSleepTime / 1e3), 2)
						}
						if ("video" === t.mediaType || t.id.toLocaleLowerCase().includes(
								"video")) {
							var i;
							if (!(i = e.get(t.id))) return;
							if (n.videoBitrate = y(8 * (t.bytesReceived - i.bytesReceived) /
									1e3 / (r.statsReportSleepTime / 1e3), 2), t.frameWidth) n
								.frameWidth = t.frameWidth, n.frameHeight = t.frameHeight;
							else if (r.videoTrack) {
								var o = r.videoTrack.getSettings();
								n.frameWidth = o.width || 0, n.frameHeight = o.height || 0
							}
							if (t.framesPerSecond) n.frameRate = t.framesPerSecond;
							else if (t.framesDecoded && i.framesDecoded) {
								var s = t.framesDecoded - i.framesDecoded,
									a = Math.floor(s / (r.statsReportSleepTime / 1e3));
								n.frameRate = a
							}
						}
					}
				})), n
			}, e.prototype.createOffer = function(e, t) {
				return void 0 === e && (e = !0), void 0 === t && (t = !0), i(this, void 0, void 0, (
					function() {
						return o(this, (function(r) {
							switch (r.label) {
								case 0:
									return [4, this.pc.createOffer({
										offerToReceiveAudio: e,
										offerToReceiveVideo: t
									})];
								case 1:
									return [2, r.sent()]
							}
						}))
					}))
			}, e.prototype.mungSDP = function(e) {
				return e
			}, e.prototype.setLocal = function(e) {
				return i(this, void 0, void 0, (function() {
					var t, r;
					return o(this, (function(n) {
						switch (n.label) {
							case 0:
								return n.trys.push([0, 2, , 3]), [4, this.pc
									.setLocalDescription(e)
								];
							case 1:
								return n.sent(), [3, 3];
							case 2:
								throw t = n.sent(), r = "set local sdp error: \n" +
									e.sdp + "\n" + g(t), I(r), new T(r);
							case 3:
								return [2]
						}
					}))
				}))
			}, e.prototype.setRemote = function(e) {
				return i(this, void 0, void 0, (function() {
					var t, r, n;
					return o(this, (function(i) {
						switch (i.label) {
							case 0:
								t = new RTCSessionDescription(e), i.label = 1;
							case 1:
								return i.trys.push([1, 3, , 4]), [4, this.pc
									.setRemoteDescription(t)
								];
							case 2:
								return i.sent(), [3, 4];
							case 3:
								throw r = i.sent(), n = "set remote sdp error: \n" +
									t.sdp + "\n" + g(r), I(n), new T(n);
							case 4:
								return [2]
						}
					}))
				}))
			}, e
		}(),
		He = function(e) {
			function t() {
				var t = e.call(this) || this;
				return t.qnPC = new We, P.on("log", (function(e) {
					t.emit("log", e)
				})), P.on("stats", (function(e) {
					t.emit("stats", e)
				})), P.on("error", (function(e) {
					t.setState(w.STATE_ERROR), t.stop(), t.emit("error", e)
				})), P.on("playerStateChanged", (function(e) {
					h.log("playerStateChanged: " + e), t.emit("playerStateChanged", e)
				})), t.setState(w.STATE_IDLE), a().then((function(e) {
					t.playerSupport = e, e.peerConnection || M("RTC not supported!"), e.H264 || M(
						"H264 not supported!")
				})), t
			}
			return r(t, e), t.prototype.setState = function(e) {
				this.playerState !== e && (this.playerState = e, function(e) {
					P.emit("playerStateChanged", e)
				}(e))
			}, t.prototype.init = function(e) {
				this.setState(w.STATE_INIT), this.config = n(n({}, C), e)
			}, t.prototype.getConfig = function() {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				return this.config
			}, t.prototype.setConfig = function(e) {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				if (!this.mediaElement) throw new T("media is not initialized, try play() first.");
				void 0 !== e.className && (this.config.className = e.className, this.mediaElement
						.className = this.config.className), void 0 !== e.controls && (this.config
						.controls = e.controls, this.mediaElement.controls = this.config.controls),
					void 0 !== e.width && (this.config.width = e.width, this.mediaElement.style.width = this
						.config.width), void 0 !== e.height && (this.config.height = e.height, this
						.mediaElement.style.height = this.config.height), void 0 !== e.objectFit && (this
						.config.objectFit = e.objectFit, this.mediaElement.style.objectFit = this.config
						.objectFit), void 0 !== e.playsinline && (this.config.playsinline = e.playsinline,
						this.mediaElement.playsInline = this.config.playsinline, this.mediaElement
						.setAttribute("webkit-playsinline", String(e.playsinline))), void 0 !== e.volumn &&
					(this.config.volumn = e.volumn, this.mediaElement.volume = this.config.volumn)
			}, t.prototype.play = function(e, t) {
				return i(this, void 0, void 0, (function() {
					var r, n = this;
					return o(this, (function(s) {
						switch (s.label) {
							case 0:
								if (!this.config) throw new T(
									"config is not initilized, try init() first."
									);
								return this.url === e && this.container === t ? [
									2] : (this.mediaElement || (this.mediaElement =
											document.createElement("video"), this
											.mediaElement.setAttribute(
												"x5-video-player-type", "h5"), this
											.setConfig(this.config)), this
										.mediaStream && this.url && this.url === e ?
										[3, 2] : (this.url = e, r = this, [4, this
											.qnPC.pullStream(this.url)
										]));
							case 1:
								r.mediaStream = s.sent(), this.setState(w
										.STATE_READY), this.mediaElement.srcObject =
									this.mediaStream, s.label = 2;
							case 2:
								return this.mediaElement && this.container && this
									.mediaElement.parentElement && this.mediaElement
									.parentElement !== this.container && this
									.mediaElement.parentElement.removeChild(this
										.mediaElement), this.container && this
									.container === t || (this.container = t, this
										.container.appendChild(this.mediaElement)),
									[2, new Promise((function(e, t) {
										var r, s, a = setTimeout((
											function() {
												n.playerState !=
													w
													.STATE_IDLE &&
													n.resume()
													.then(e)
													.catch(t)
											}), b);
										n.mediaElement.addEventListener(
												"loadedmetadata", (
													function() {
														clearTimeout(a),
															n
															.playerState !=
															w
															.STATE_IDLE &&
															n.resume()
															.then(e)
															.catch(t)
													})), r =
										function() {
												return i(n, void 0,
													void 0, (
														function() {
															return o(
																this,
																(function(
																	e
																	) {
																	return this
																		.playerState !=
																		w
																		.STATE_IDLE ?
																		[2, this
																			.resume()
																		] :
																		[
																			2]
																})
																)
														}))
											}, void 0 === s && (s =
											5e3), new Promise((function(
												e, t) {
												if ("WeixinJSBridge" in
													window)
													window
													.WeixinJSBridge
													.invoke(
														"getNetworkType", {},
														(function() {
															r().then(
																	e
																	)
																.catch(
																	t
																	)
														}), !1);
												else {
													var n =
														setTimeout(
															(function() {
																r().then(
																		e
																		)
																	.catch(
																		t
																		)
															}),
															s);
													document
														.addEventListener(
															"WeixinJSBridgeReady",
															(function() {
																clearTimeout
																	(
																		n),
																	r()
																	.then(
																		e
																		)
																	.catch(
																		t
																		)
															}),
															!1)
												}
											}))
									}))]
						}
					}))
				}))
			}, t.prototype.pause = function() {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				if (!this.mediaElement) throw new T("media is not initialized, try play() first.");
				this.mediaElement.pause()
			}, t.prototype.resume = function() {
				var e = this;
				return new Promise((function(t, r) {
					if (!e.config) throw new T("config is not initilized, try init() first.");
					if (!e.mediaElement) throw new T(
						"media is not initialized, try play() first.");
					e.isPlaying() && t();
					try {
						var n = e.mediaElement.play();
						n ? n.then((function() {
							e.playerState !== w.STATE_STOP && e.setState(w
								.STATE_PLAYING), t()
						})).catch((function(e) {
							if ("NotAllowedError" === e.name) {
								var n = "play fail, " + e.name + ", " + e.message;
								r(new T(n))
							} else t()
						})) : (e.playerState !== w.STATE_STOP && e.setState(w
							.STATE_PLAYING), t())
					} catch (e) {
						var i = e instanceof Error ? "play error, " + e.name + ", " + e
							.message : String(e);
						r(new T(i))
					}
				}))
			}, t.prototype.hasAudio = function() {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				if (!this.mediaElement) throw new T("media is not initialized, try play() first.");
				return !!this.mediaStream && this.mediaStream.getAudioTracks().length > 0
			}, t.prototype.hasVideo = function() {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				if (!this.mediaElement) throw new T("media is not initialized, try play() first.");
				return !!this.mediaStream && this.mediaStream.getVideoTracks().length > 0
			}, t.prototype.setAudioVolume = function(e) {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				if (!this.mediaElement) throw new T("media is not initialized, try play() first.");
				this.mediaElement.volume = e
			}, t.prototype.getAudioVolume = function() {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				if (!this.mediaElement) throw new T("media is not initialized, try play() first.");
				return this.mediaElement.volume
			}, t.prototype.muteAudio = function() {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				if (!this.mediaElement) throw new T("media is not initialized, try play() first.");
				this.mediaElement.muted = !0
			}, t.prototype.unmuteAudio = function() {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				if (!this.mediaElement) throw new T("media is not initialized, try play() first.");
				this.mediaElement.muted = !1
			}, t.prototype.muteVideo = function() {
				var e;
				if (!this.config) throw new T("config is not initilized, try init() first.");
				if (!this.mediaElement) throw new T("media is not initialized, try play() first.");
				var t = null === (e = this.mediaStream) || void 0 === e ? void 0 : e.getAudioTracks();
				t && t.length > 0 ? this.mediaElement.srcObject = new MediaStream(t) : this.mediaElement
					.srcObject = null, this.resume()
			}, t.prototype.unmuteVideo = function() {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				if (!this.mediaElement) throw new T("media is not initialized, try play() first.");
				if (!this.mediaStream) throw new T("mediaStream is empty");
				this.mediaElement.srcObject = this.mediaStream, this.resume()
			}, t.prototype.isPlaying = function() {
				return !!this.mediaElement && !this.mediaElement.paused
			}, t.prototype.stop = function() {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				if (!this.mediaElement) throw new T("media is not initialized, try play() first.");
				this.qnPC.release(), this.url = void 0, this.setState(w.STATE_STOP)
			}, t.prototype.release = function() {
				if (!this.config) throw new T("config is not initilized, try init() first.");
				this.setState(w.STATE_IDLE), this.config = void 0, this.mediaElement && this.mediaElement
					.parentElement && this.mediaElement.parentElement.removeChild(this.mediaElement), this
					.qnPC.release(), this.url = void 0, this.mediaElement = void 0, this.container = void 0,
					this.mediaStream = void 0
			}, t.prototype.getPlayerSupport = function() {
				return this.playerSupport
			}, t.prototype.getBrowserReport = function() {
				return l
			}, Object.defineProperty(t.prototype, "version", {
				get: function() {
					return R
				},
				enumerable: !1,
				configurable: !0
			}), t.setLogLevel = function(e) {
				h.setLevel(e)
			}, t
		}(E);
	e.QNRTPlayer = He, Object.defineProperty(e, "__esModule", {
		value: !0
	})
}));

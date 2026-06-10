import os, math, uuid, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import folder_paths

TRANSITION_MAP = {
    '叠化': 'crossfade',
    '叠加': 'crossfade',
    '色彩溶解': 'crossfade',
    '色彩溶解 II': 'crossfade',
    '色彩溶解 III': 'crossfade',
    '右移': 'slide_right',
    '向右': 'slide_right',
    '向右擦除': 'wipe_right',
    '左移': 'slide_left',
    '向左': 'slide_left',
    '向左擦除': 'wipe_left',
    '上移': 'slide_up',
    '向上': 'slide_up',
    '向上擦除': 'wipe_up',
    '下移': 'slide_down',
    '向下': 'slide_down',
    '向下擦除': 'wipe_down',
    '泛白': 'fade_white',
    '白光快闪': 'flash_white',
    '闪黑 II': 'fade_black',
    '推近': 'zoom_in',
    '拉远': 'zoom_out',
    '拉伸': 'stretch',
    '拉伸 II': 'stretch',
    '模糊': 'dissolve_blur',
    '竖向模糊': 'dissolve_blur',
    '圆形遮罩': 'circle_reveal',
    '圆形遮罩 II': 'circle_reveal',
    '圆形扫描': 'circle_reveal',
    '横向拉幕': 'wipe_right',
    '竖向拉幕': 'wipe_down',
    '开幕': 'curtain_open',
    '分割': 'split_h',
    '分割 II': 'split_h',
    '分割 III': 'split_v',
    '竖向分割': 'split_v',
    '横向分割': 'split_h',
    '斜向分割': 'split_diagonal',
    '百叶窗': 'blinds',
    '百叶窗 II': 'blinds',
    '中心旋转': 'rotate',
    '故障': 'glitch',
    '电视故障 I': 'glitch',
    '电视故障 II': 'glitch',
    '弹跳': 'bounce',
    '爱心': 'heart_reveal',
    '星星': 'star_reveal',
    '云朵': 'cloud',
    '动漫云朵': 'cloud',
    '翻页': 'flip',
    '翻篇': 'flip',
    '窗格': 'window_grid',
    '横线': 'line_wipe_h',
    '竖线': 'line_wipe_v',
    '吸入': 'suck_in',
    '复古放映': 'vintage',
    '抖动': 'shake',
    '抖动 II': 'shake',
    '滑动': 'slide_right',
    '回忆下滑': 'slide_down',
    '渐变擦除': 'crossfade',
    '向右流动': 'slide_right',
    '向左流动': 'slide_left',
    '向下流动': 'slide_down',
    '向右拉伸': 'slide_right',
    '向左拉伸': 'slide_left',
    '泛光': 'glow',
    '水波卷动': 'crossfade',
    '水波向右': 'slide_right',
    '水波向左': 'slide_left',
    '色差逆时针': 'rotate',
    '色差顺时针': 'rotate',
    '圆形分割_II': 'circle_reveal',
    '左下角_II': 'slide_left',
    '前后对比 II': 'crossfade',
    '岁月的痕迹': 'vintage',
    '压缩': 'zoom_in',
    '扩散': 'zoom_out',
    '箭头向右': 'arrow_right',
    '粒子': 'particles',
    '气泡转场': 'bubbles',
    '弹幕转场': 'danmaku',
    '冲鸭': 'slide_right',
    '倒影': 'reflection',
    '冰雪结晶': 'freeze',
    '立方体': 'cube_rotate',
}

DEFAULT_TRANSITION = 'crossfade'

INTRO_ANIMATION_MAP = {
    '渐显': 'fade_in',
    '放大': 'zoom_in',
    '缩小': 'zoom_in_from_small',
    '旋转': 'rotate_in',
    '向左滑动': 'slide_in_left',
    '向右滑动': 'slide_in_right',
    '向上滑动': 'slide_in_up',
    '向下滑动': 'slide_in_down',
    '镜像翻转': 'mirror_flip_in',
    '轻微抖动': 'shake',
    '轻微抖动 II': 'shake',
    '轻微抖动 III': 'shake',
    '上下抖动': 'shake_v',
    '左右抖动': 'shake_h',
    '抖动下降': 'shake_drop',
    '旋转开幕': 'rotate_open',
    '漩涡旋转': 'swirl_in',
    '钟摆': 'pendulum',
    '雨刷': 'wiper',
    '向上转入': 'rotate_in_up',
    '向上转入 II': 'rotate_in_up',
    '向左转入': 'rotate_in_left',
    '向右转入': 'rotate_in_right',
    '向下甩入': 'swing_in_down',
    '向右甩入': 'swing_in_right',
    '向左上甩入': 'swing_in_left_up',
    '向右上甩入': 'swing_in_right_up',
    '向左下甩入': 'swing_in_left_down',
    '向右下甩入': 'swing_in_right_down',
    '动感放大': 'dynamic_zoom_in',
    '动感缩小': 'dynamic_zoom_out',
    '轻微放大': 'slight_zoom_in',
    '折叠开幕': 'fold_open',
    '跳转开幕': 'jump_open',
}

DEFAULT_INTRO = 'fade_in'

OUTRO_ANIMATION_MAP = {
    '渐隐': 'fade_out',
    '放大': 'zoom_out_big',
    '缩小': 'zoom_out',
    '旋转': 'rotate_out',
    '向上滑动': 'slide_out_up',
    '向下滑动': 'slide_out_down',
    '向左滑动': 'slide_out_left',
    '向右滑动': 'slide_out_right',
    '镜像翻转': 'mirror_flip_out',
    '旋转闭幕': 'rotate_close',
    '漩涡旋转': 'swirl_out',
    '向上转出': 'rotate_out_up',
    '向上转出 II': 'rotate_out_up',
    '轻微放大': 'slight_zoom_out',
    '折叠闭幕': 'fold_close',
    '跳转闭幕': 'jump_close',
}

DEFAULT_OUTRO = 'fade_out'
EFFECT_MAP = {
    "模糊": "blur",
    "马赛克": "mosaic",
    "低像素": "pixelate",
    "低像素_II": "pixelate",
    "像素": "pixelate",
    "变亮": "brighten",
    "提亮": "brighten",
    "变暗": "darken",
    "压暗": "darken",
    "灰度": "grayscale",
    "黑白": "grayscale",
    "黑白电影": "grayscale",
    "黑白胶片": "grayscale",
    "复古": "sepia",
    "怀旧": "sepia",
    "做旧": "sepia",
    "暖色": "warm",
    "冷色": "cool",
    "反色": "invert",
    "反转": "invert",
    "镜像": "mirror_h",
    "左右镜像": "mirror_h",
    "上下镜像": "mirror_v",
    "锐化": "sharpen",
    "毛刺": "glitch",
    "色差": "chromatic",
    "重影": "ghost",
}


# Image extensions
IMAGE_EXTENSIONS = {'.png','.jpg','.jpeg','.bmp','.webp','.tiff','.tif'}

FONT_MAP = {
    '宋体': 'simsun.ttc',
    '新宋体': 'simsun.ttc',
    '黑体': 'simhei.ttf',
    '微软雅黑': 'msyh.ttc',
    '楷体': 'simkai.ttf',
    '仿宋': 'simfang.ttf',
    '隶书': 'SIMLI.TTF',
    '幼圆': 'SIMYOU.TTF',
}

font_dir = os.path.abspath(os.path.join(__file__, "../../fonts"))
if not os.path.exists(font_dir):
    os.mkdir(font_dir)

def is_image_file(path):
    return os.path.splitext(path)[1].lower() in IMAGE_EXTENSIONS

def get_font_pil(font_name, font_size):
    candidates = []
    if font_name in FONT_MAP:
        candidates.append(os.path.join(font_dir, FONT_MAP[font_name]))
    for ext in ['.ttf', '.ttc']:
        candidates.append(os.path.join(font_dir, font_name + ext))
    candidates.append(os.path.join(font_dir, 'msyh.ttc'))
    for fp in candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, font_size)
            except:
                pass
    try:
        return ImageFont.load_default()
    except:
        pass
    # Last resort: try any available system font
    try:
        return ImageFont.truetype('arial.ttf', font_size)
    except:
        pass
    return None

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def make_transition_frame(frame_a, frame_b, progress, trans_type, w, h):
    p = max(0.0, min(1.0, progress))
    fa = frame_a.astype(np.float32)
    fb = frame_b.astype(np.float32)
    if trans_type == 'crossfade':
        return np.clip(fa * (1 - p) + fb * p, 0, 255).astype(np.uint8)
    elif trans_type == 'fade_black':
        if p < 0.5: return np.clip(fa * (1 - p * 2), 0, 255).astype(np.uint8)
        else: return np.clip(fb * ((p - 0.5) * 2), 0, 255).astype(np.uint8)
    elif trans_type in ('fade_white', 'flash_white'):
        if p < 0.5:
            pp = p * 2
            return np.clip(fa * (1 - pp) + 255 * pp, 0, 255).astype(np.uint8)
        else:
            pp = (p - 0.5) * 2
            return np.clip(fb * pp + 255 * (1 - pp), 0, 255).astype(np.uint8)
    elif trans_type in ('slide_right', 'slide_left', 'slide_up', 'slide_down'):
        offset = int((w if trans_type in ('slide_right', 'slide_left') else h) * p)
        result = fa.copy()
        if trans_type == 'slide_right':
            if offset < w: result[:, :w - offset] = fa[:, offset:]; result[:, w - offset:] = fb[:, :offset]
        elif trans_type == 'slide_left':
            if offset < w: result[:, offset:] = fa[:, :w - offset]; result[:, :offset] = fb[:, w - offset:]
        elif trans_type == 'slide_up':
            if offset < h: result[:h - offset, :] = fa[offset:, :]; result[h - offset:, :] = fb[:offset, :]
        elif trans_type == 'slide_down':
            if offset < h: result[offset:, :] = fa[:h - offset, :]; result[:offset, :] = fb[h - offset:, :]
        return np.clip(result, 0, 255).astype(np.uint8)
    elif trans_type.startswith('wipe_'):
        if trans_type == 'wipe_right':
            x = int(w * p); result = fa.copy(); result[:, :x] = fb[:, :x]; return result
        elif trans_type == 'wipe_left':
            x = int(w * p); result = fa.copy(); result[:, w - x:] = fb[:, w - x:]; return result
        elif trans_type == 'wipe_up':
            y = int(h * p); result = fa.copy(); result[:y, :] = fb[:y, :]; return result
        elif trans_type == 'wipe_down':
            y = int(h * p); result = fa.copy(); result[h - y:, :] = fb[h - y:, :]; return result
        return np.clip(fa * (1 - p) + fb * p, 0, 255).astype(np.uint8)
    elif trans_type == 'circle_reveal':
        cx, cy = w // 2, h // 2
        max_r = int(math.sqrt(cx * cx + cy * cy))
        r = int(max_r * p)
        Y, X = np.ogrid[:h, :w]
        mask = ((X - cx) ** 2 + (Y - cy) ** 2 <= r * r)[:, :, np.newaxis]
        return np.where(mask, fb, fa).astype(np.uint8)
    elif trans_type == 'zoom_in':
        scale = 1 + p * 0.5; nw, nh = max(int(w / scale), 1), max(int(h / scale), 1)
        img_a = Image.fromarray(frame_a)
        crop = img_a.crop(((w - nw) // 2, (h - nh) // 2, (w + nw) // 2, (h + nh) // 2))
        fa_zoom = np.array(crop.resize((w, h), Image.LANCZOS)).astype(np.float32)
        return np.clip(fa_zoom * (1 - p) + fb * p, 0, 255).astype(np.uint8)
    elif trans_type == 'zoom_out':
        scale = max(p, 0.01); nw, nh = max(int(w * scale), 1), max(int(h * scale), 1)
        img_b = Image.fromarray(frame_b)
        fb_small = np.array(img_b.resize((nw, nh), Image.LANCZOS))
        result = fa.copy()
        xo, yo = (w - nw) // 2, (h - nh) // 2
        x1, x2 = max(0, xo), min(w, xo + nw)
        y1, y2 = max(0, yo), min(h, yo + nh)
        if y2 > y1 and x2 > x1:
            result[y1:y2, x1:x2] = fb_small[y1 - yo:y2 - yo, x1 - xo:x2 - xo]
        return result
    elif trans_type == 'dissolve_blur':
        return np.clip(fa * (1 - p) + fb * p, 0, 255).astype(np.uint8)
    elif trans_type == 'split_h':
        result = fa.copy(); stripe_h = max(h // 10, 1)
        for i in range(0, h, stripe_h):
            end_y = min(i + stripe_h, h)
            reveal_end = i + int((end_y - i) * p)
            result[i:reveal_end, :] = fb[i:reveal_end, :]
        return result
    elif trans_type == 'split_v':
        result = fa.copy(); stripe_w = max(w // 10, 1)
        for i in range(0, w, stripe_w):
            end_x = min(i + stripe_w, w)
            reveal_end = i + int((end_x - i) * p)
            result[:, i:reveal_end] = fb[:, i:reveal_end]
        return result
    elif trans_type == 'blinds':
        result = fa.copy(); stripe_h = max(h // 12, 1)
        for i in range(0, h, stripe_h):
            end_y = min(i + stripe_h, h)
            reveal_end = i + int((end_y - i) * p)
            result[i:reveal_end, :] = fb[i:reveal_end, :]
        return result
    elif trans_type == 'rotate':
        angle = p * 360
        img_a = Image.fromarray(frame_a).rotate(angle, resample=Image.BICUBIC, expand=False)
        fa_rot = np.array(img_a).astype(np.float32)
        return np.clip(fa_rot * (1 - p) + fb * p, 0, 255).astype(np.uint8)
    elif trans_type == 'flip':
        if p < 0.5:
            pp = p * 2; nw = max(int(w * (1 - pp)), 1)
            img_a = Image.fromarray(frame_a).resize((nw, h), Image.LANCZOS)
            result = np.zeros((h, w, 3), dtype=np.uint8)
            xo = (w - nw) // 2; result[:, xo:xo + nw] = np.array(img_a)
        else:
            pp = (p - 0.5) * 2; nw = max(int(w * pp), 1)
            img_b = Image.fromarray(frame_b).resize((nw, h), Image.LANCZOS)
            result = np.zeros((h, w, 3), dtype=np.uint8)
            xo = (w - nw) // 2; result[:, xo:xo + nw] = np.array(img_b)
        return result
    elif trans_type == 'glitch':
        result = fa.copy()
        if np.random.random() < 0.4:
            shift = np.random.randint(-15, 15); result = np.roll(result, shift, axis=1)
        if np.random.random() < 0.3:
            r_shift = np.random.randint(3, 10)
            result[:, :, 0] = np.roll(result[:, :, 0], r_shift, axis=1)
            result[:, :, 2] = np.roll(result[:, :, 2], -r_shift, axis=1)
        return np.clip(result.astype(np.float32) * (1 - p) + fb * p, 0, 255).astype(np.uint8)
    elif trans_type == 'bounce':
        if p < 0.7:
            bp = p / 0.7; by = int(-h * 0.3 * (1 - bp))
        else:
            bp = (p - 0.7) / 0.3; by = int(-h * 0.1 * math.sin(bp * math.pi))
        result = fa.copy()
        if by >= 0: result[by:, :] = fb[:h - by, :]
        else: result[:h + by, :] = fb[-by:, :]
        return result
    elif trans_type == 'shake':
        amp = 12 * (1 - p) if p < 0.8 else 2.4
        sx = int(amp * math.sin(p * 25)); sy = int(amp * math.cos(p * 20))
        result = np.roll(np.roll(fa, sx, axis=1), sy, axis=0)
        return np.clip(result.astype(np.float32) * (1 - p) + fb * p, 0, 255).astype(np.uint8)
    elif trans_type == 'vintage':
        r = fa.copy(); r[:, :, 0] = np.clip(r[:, :, 0] * 1.15, 0, 255)
        r[:, :, 2] = np.clip(r[:, :, 2] * 0.75, 0, 255)
        return np.clip(r.astype(np.float32) * (1 - p) + fb * p, 0, 255).astype(np.uint8)
    elif trans_type == 'stretch':
        scale = max(1 - p, 0.01); nw = max(int(w * scale), 1)
        img_a = Image.fromarray(frame_a).resize((nw, h), Image.LANCZOS)
        result = np.zeros((h, w, 3), dtype=np.uint8)
        xo = (w - nw) // 2; result[:, xo:xo + nw] = np.array(img_a)
        return np.where(p > 0.5, fb, result).astype(np.uint8)
    elif trans_type == 'curtain_open':
        mid = w // 2; offset = int(mid * (1 - p))
        result = fa.copy()
        result[:, :offset] = 0; result[:, w - offset:] = 0
        if w - 2 * offset > 0:
            result[:, offset:w - offset] = fb[:, offset:w - offset]
        return result
    elif trans_type == 'split_diagonal':
        result = fa.copy()
        for y in range(h):
            threshold = int(w * p)
            result[y, :min(threshold, w)] = fb[y, :min(threshold, w)]
        return result
    else:
        return np.clip(fa * (1 - p) + fb * p, 0, 255).astype(np.uint8)

def apply_intro_frame(frame, t, anim_type, duration, w, h):
    if t >= duration: return frame
    p = max(0.0, min(1.0, t / duration))
    return _apply_anim_core(frame, p, anim_type, w, h, True)

def apply_outro_frame(frame, t, anim_type, duration, w, h, clip_dur):
    remaining = clip_dur - t
    if remaining >= duration: return frame
    p = max(0.0, min(1.0, remaining / duration))
    return _apply_anim_core(frame, p, anim_type, w, h, False)

def _apply_anim_core(frame, p, anim_type, w, h, is_intro):
    if anim_type in ('fade_in', 'fade_out'):
        return np.clip(frame.astype(np.float32) * p, 0, 255).astype(np.uint8)
    elif anim_type in ('zoom_in', 'zoom_in_from_small', 'slight_zoom_in', 'dynamic_zoom_in'):
        s = (0.2 + 0.8 * p) if is_intro else (1.0 + 0.6 * (1 - p))
        nw, nh = max(int(w * s), 1), max(int(h * s), 1)
        img = Image.fromarray(frame).resize((nw, nh), Image.LANCZOS)
        result = np.zeros((h, w, 3), dtype=np.uint8)
        xo, yo = (w - nw) // 2, (h - nh) // 2
        cw, ch = min(nw, w - xo), min(nh, h - yo)
        if ch > 0 and cw > 0: result[yo:yo + ch, xo:xo + cw] = np.array(img)[:ch, :cw]
        if not is_intro:
            result = np.clip(result.astype(np.float32) * (0.5 + 0.5 * p), 0, 255).astype(np.uint8)
        return result
    elif anim_type in ('zoom_out', 'zoom_out_big', 'slight_zoom_out', 'dynamic_zoom_out'):
        s = max((1.5 - 0.5 * p) if is_intro else (1.0 - 0.8 * (1 - p)), 0.01)
        nw, nh = max(int(w * s), 1), max(int(h * s), 1)
        img = Image.fromarray(frame).resize((nw, nh), Image.LANCZOS)
        if nw <= w and nh <= h:
            result = np.zeros((h, w, 3), dtype=np.uint8)
            xo, yo = (w - nw) // 2, (h - nh) // 2
            result[yo:yo + nh, xo:xo + nw] = np.array(img)
        else:
            cx, cy = nw // 2, nh // 2
            result = np.array(img)[cy - h // 2:cy + h // 2, cx - w // 2:cx + w // 2]
        if not is_intro:
            result = np.clip(result.astype(np.float32) * (0.5 + 0.5 * p), 0, 255).astype(np.uint8)
        return result
    elif anim_type in ('slide_in_left', 'slide_out_left'):
        off = int(w * (1 - p)); result = np.zeros((h, w, 3), dtype=np.uint8)
        if is_intro: result[:, off:] = frame[:, :w - off]
        else: result[:, :w - off] = frame[:, off:]
        return result
    elif anim_type in ('slide_in_right', 'slide_out_right'):
        off = int(w * (1 - p)); result = np.zeros((h, w, 3), dtype=np.uint8)
        if is_intro: result[:, :w - off] = frame[:, off:]
        else: result[:, off:] = frame[:, :w - off]
        return result
    elif anim_type in ('slide_in_up', 'slide_out_up'):
        off = int(h * (1 - p)); result = np.zeros((h, w, 3), dtype=np.uint8)
        if is_intro: result[off:, :] = frame[:h - off, :]
        else: result[:h - off, :] = frame[off:, :]
        return result
    elif anim_type in ('slide_in_down', 'slide_out_down'):
        off = int(h * (1 - p)); result = np.zeros((h, w, 3), dtype=np.uint8)
        if is_intro: result[:h - off, :] = frame[off:, :]
        else: result[off:, :] = frame[:h - off, :]
        return result
    elif anim_type in ('rotate_in', 'rotate_out', 'rotate_open', 'rotate_close'):
        angle = ((1 - p) * 360) if is_intro else (p * 360)
        img = Image.fromarray(frame).rotate(angle, resample=Image.BICUBIC, expand=False)
        result = np.array(img).astype(np.float32)
        return np.clip(result * max(p, 0.3) + frame.astype(np.float32) * (1 - max(p, 0.3)), 0, 255).astype(np.uint8)
    elif anim_type in ('mirror_flip_in', 'mirror_flip_out'):
        s = abs(math.sin(math.pi / 2 * (p if is_intro else (1 - p))))
        nw = max(int(w * s), 1)
        img = Image.fromarray(frame).resize((nw, h), Image.LANCZOS)
        result = np.zeros((h, w, 3), dtype=np.uint8)
        xo = (w - nw) // 2; result[:, xo:xo + nw] = np.array(img)
        return result
    elif anim_type == 'shake':
        amp = 15 * (1 - p)
        sx, sy = int(amp * math.sin(p * 30)), int(amp * math.cos(p * 25))
        return np.roll(np.roll(frame, sx, axis=1), sy, axis=0)
    elif anim_type == 'shake_v':
        return np.roll(frame, int(15 * (1 - p) * math.sin(p * 30)), axis=0)
    elif anim_type == 'shake_h':
        return np.roll(frame, int(15 * (1 - p) * math.sin(p * 30)), axis=1)
    elif anim_type == 'shake_drop':
        return np.roll(frame, int(10 * (1 - p) * 3), axis=0)
    elif anim_type == 'swirl_in' or anim_type == 'swirl_out':
        angle = 720 * (1 - p) if is_intro else 720 * p
        img = Image.fromarray(frame).rotate(angle, resample=Image.BICUBIC, expand=False)
        return np.clip(np.array(img).astype(np.float32) * p, 0, 255).astype(np.uint8)
    elif anim_type in ('fold_open', 'fold_close'):
        if (is_intro and anim_type == 'fold_open') or (not is_intro and anim_type == 'fold_close'):
            nw = max(int(w * p), 1)
            img = Image.fromarray(frame).resize((nw, h), Image.LANCZOS)
            result = np.zeros((h, w, 3), dtype=np.uint8)
            xo = (w - nw) // 2; result[:, xo:xo + nw] = np.array(img)
            return result
    elif anim_type in ('jump_open', 'jump_close'):
        s = 0.5 + 0.5 * (p if is_intro else (1 - p))
        nw, nh = max(int(w * s), 1), max(int(h * s), 1)
        img = Image.fromarray(frame).resize((nw, nh), Image.LANCZOS)
        result = np.zeros((h, w, 3), dtype=np.uint8)
        xo, yo = (w - nw) // 2, (h - nh) // 2
        cw, ch = min(nw, w - xo), min(nh, h - yo)
        if ch > 0 and cw > 0: result[yo:yo + ch, xo:xo + cw] = np.array(img)[:ch, :cw]
        return result
    elif anim_type in ('swing_in_down', 'swing_in_right', 'swing_in_left_up', 'swing_in_right_up', 'swing_in_left_down', 'swing_in_right_down'):
        dx_map = {'swing_in_down': 0, 'swing_in_right': -1, 'swing_in_left_up': 1, 'swing_in_right_up': -1, 'swing_in_left_down': 1, 'swing_in_right_down': -1}
        dy_map = {'swing_in_down': -1, 'swing_in_right': 0, 'swing_in_left_up': -1, 'swing_in_right_up': -1, 'swing_in_left_down': 1, 'swing_in_right_down': 1}
        dx, dy = dx_map.get(anim_type, 0), dy_map.get(anim_type, 0)
        off_x, off_y = int(w * dx * (1 - p) * 0.5), int(h * dy * (1 - p) * 0.5)
        result = np.zeros((h, w, 3), dtype=np.uint8)
        x1, x2 = max(0, off_x), min(w, w + off_x)
        y1, y2 = max(0, off_y), min(h, h + off_y)
        sx1, sx2 = max(0, -off_x), min(w - off_x, w)
        sy1, sy2 = max(0, -off_y), min(h - off_y, h)
        if y2 > y1 and x2 > x1:
            result[y1:y2, x1:x2] = frame[sy1:sy2, sx1:sx2]
        return result
    else:
        return np.clip(frame.astype(np.float32) * p, 0, 255).astype(np.uint8)

def render_subtitle(text, font_name, font_size_pct, color_hex, width, height, transform_x, transform_y):
    r, g, b = hex_to_rgb(color_hex)
    actual_size = max(int(font_size_pct * height / 300), 10)
    font = get_font_pil(font_name, actual_size)
    if font is None:
        print(f'[JyComposeVideo] Font not found: {font_name}, using default')
        try:
            font = ImageFont.truetype(r'C:\\Windows\\Fonts\\msyh.ttc', actual_size)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
    if font is None:
        raise RuntimeError('No usable font found for subtitle rendering')
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    lines = text.split('\n')
    line_info = [(draw.textbbox((0, 0), l, font=font)[2] - draw.textbbox((0, 0), l, font=font)[0],
                  draw.textbbox((0, 0), l, font=font)[3] - draw.textbbox((0, 0), l, font=font)[1]) for l in lines]
    max_lw = max((lw for lw, _ in line_info)) if line_info else 0
    total_h = sum(lh for _, lh in line_info) + (len(lines) - 1) * 4
    center_x = width // 2 + int(transform_x * width / 2)
    center_y = height // 2 - int(transform_y * height / 2)
    start_y = center_y - total_h // 2
    current_y = start_y
    for i, line in enumerate(lines):
        lw, lh = line_info[i]
        x = center_x - lw // 2
        outline_w = max(1, actual_size // 25)
        for ox in range(-outline_w, outline_w + 1):
            for oy in range(-outline_w, outline_w + 1):
                if ox * ox + oy * oy <= outline_w * outline_w:
                    draw.text((x + ox, current_y + oy), line, font=font, fill=(0, 0, 0, 200))
        draw.text((x, current_y), line, font=font, fill=(r, g, b, 255))
        current_y += lh + 4
    return np.array(img)

def apply_effect_frame(frame, effect_name, t, duration, w, h):
    import math
    p = min(t / max(duration, 0.001), 1.0) if duration > 0 else 0.5
    eff_key = EFFECT_MAP.get(effect_name)
    if not eff_key:
        ename_lower = effect_name.lower()
        for k, v in EFFECT_MAP.items():
            if k in effect_name or ename_lower in k.lower():
                eff_key = v
                break
    if not eff_key:
        return frame

    if eff_key == "blur":
        ksize = int(3 + 20 * p)
        if ksize % 2 == 0:
            ksize += 1
        if ksize > 31:
            ksize = 31
        img = Image.fromarray(frame)
        return np.array(img.filter(ImageFilter.GaussianBlur(ksize)))

    elif eff_key in ("mosaic", "pixelate"):
        block = max(2, int(3 + 40 * p))
        h_img, w_img = frame.shape[:2]
        small_w, small_h = max(w_img // block, 1), max(h_img // block, 1)
        img = Image.fromarray(frame)
        small = img.resize((small_w, small_h), Image.NEAREST)
        return np.array(small.resize((w_img, h_img), Image.NEAREST))

    elif eff_key == "brighten":
        factor = 1.0 + 0.6 * p
        return np.clip(frame.astype(np.float32) * factor, 0, 255).astype(np.uint8)

    elif eff_key == "darken":
        factor = 1.0 - 0.6 * p
        return np.clip(frame.astype(np.float32) * factor, 0, 255).astype(np.uint8)

    elif eff_key == "grayscale":
        gray = np.dot(frame[..., :3], [0.299, 0.587, 0.114])
        alpha = 0.3 + 0.7 * p
        blend = frame.astype(np.float32) * (1 - alpha) + np.stack([gray, gray, gray], axis=-1) * alpha
        return np.clip(blend, 0, 255).astype(np.uint8)

    elif eff_key == "sepia":
        gray = np.dot(frame[..., :3], [0.299, 0.587, 0.114])
        r = np.clip(gray * 1.15, 0, 255)
        g = np.clip(gray * 0.87, 0, 255)
        b = np.clip(gray * 0.65, 0, 255)
        sepia_frame = np.stack([r, g, b], axis=-1).astype(np.uint8)
        alpha = 0.3 + 0.7 * p
        return np.clip(frame.astype(np.float32) * (1 - alpha) + sepia_frame.astype(np.float32) * alpha, 0, 255).astype(np.uint8)

    elif eff_key == "warm":
        f = frame.astype(np.float32)
        warmth = 0.2 + 0.3 * p
        f[..., 0] = np.clip(f[..., 0] * (1.0 + warmth), 0, 255)
        f[..., 2] = np.clip(f[..., 2] * (1.0 - warmth), 0, 255)
        return f.astype(np.uint8)

    elif eff_key == "cool":
        f = frame.astype(np.float32)
        coolness = 0.2 + 0.3 * p
        f[..., 0] = np.clip(f[..., 0] * (1.0 - coolness), 0, 255)
        f[..., 2] = np.clip(f[..., 2] * (1.0 + coolness), 0, 255)
        return f.astype(np.uint8)

    elif eff_key == "invert":
        alpha = 0.3 + 0.7 * p
        inverted = 255 - frame
        return np.clip(frame.astype(np.float32) * (1 - alpha) + inverted.astype(np.float32) * alpha, 0, 255).astype(np.uint8)

    elif eff_key == "mirror_h":
        return frame[:, ::-1, :]
    elif eff_key == "mirror_v":
        return frame[::-1, :, :]

    elif eff_key == "sharpen":
        img = Image.fromarray(frame)
        sharp = img.filter(ImageFilter.SHARPEN)
        alpha = 0.3 + 0.7 * p
        return np.clip(frame.astype(np.float32) * (1 - alpha) + np.array(sharp).astype(np.float32) * alpha, 0, 255).astype(np.uint8)

    elif eff_key == "glitch":
        result = frame.copy()
        if p > 0.1:
            shift = int(3 + 10 * p * math.sin(t * 30))
            result = np.roll(result, shift, axis=1)
            r_shift = int(2 + 5 * p)
            if result.shape[2] >= 3:
                result[..., 0] = np.roll(result[..., 0], r_shift, axis=1)
                result[..., 2] = np.roll(result[..., 2], -r_shift, axis=1)
        return np.clip(result, 0, 255).astype(np.uint8)

    elif eff_key == "chromatic":
        r_shift = int(2 + 8 * p * math.sin(t * 15))
        result = frame.copy()
        if result.shape[2] >= 3:
            result[..., 0] = np.roll(result[..., 0], r_shift, axis=1)
            result[..., 2] = np.roll(result[..., 2], -r_shift, axis=1)
        return result

    elif eff_key == "ghost":
        alpha = 0.1 + 0.25 * p
        shifted = np.roll(frame, int(5 + 10 * p), axis=0)
        return np.clip(frame.astype(np.float32) * (1 - alpha) + shifted.astype(np.float32) * alpha, 0, 255).astype(np.uint8)

    return frame



_SLIDE_IN_MAP = {'slide_in_left': 'left', 'slide_in_right': 'right', 'slide_in_up': 'top', 'slide_in_down': 'bottom'}
_SLIDE_OUT_MAP = {'slide_out_left': 'left', 'slide_out_right': 'right', 'slide_out_up': 'top', 'slide_out_down': 'bottom'}

class JyComposeVideo:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'medias': ('MEIDA_GROUP',),
                'draft_name': ('STRING', {'default': 'ComposeVideo', 'tooltip': '视频名称'}),
                'width': ('INT', {'default': 1920, 'min': 1, 'max': 9999999, 'step': 1}),
                'height': ('INT', {'default': 1080, 'min': 1, 'max': 9999999, 'step': 1}),
                'fps': ('INT', {'default': 30, 'min': 1, 'max': 120, 'step': 1}),
            },
            'optional': {
                'audios': ('AUDIO_GROUP',),
                'effects': ('EFFECT_GROUP',),
                'captions': ('CAPTIONS_GROUP',),
                'track0': ('TRACK',),
            }
        }

    RETURN_TYPES = ('STRING', 'FLOAT')
    RETURN_NAMES = ('视频路径', '视频时长')
    FUNCTION = 'compose_video'
    OUTPUT_NODE = False
    CATEGORY = 'lam'

    def compose_video(self, medias, draft_name, width, height, fps=30, audios=[], effects=[], captions=[], **kwargs):
        from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, concatenate_videoclips, VideoClip, ColorClip, ImageClip
        from moviepy.video import fx as _vfx

        video_tracks = []
        if medias: video_tracks.append(list(medias))
        audio_tracks = []
        if audios: audio_tracks.append(list(audios))
        caption_tracks = []
        if captions: caption_tracks.append(list(captions))
        effect_tracks = []
        if effects: effect_tracks.append(list(effects))
        track_keys = [a for a in kwargs if a.startswith('track')]
        print(f'[JyComposeVideo] Found {len(track_keys)} tracks: {track_keys}')
        for arg in track_keys:
                trk = kwargs[arg]
                if not isinstance(trk, dict): continue
                tn = str(trk.get('track_type', '')).lower()
                grp = trk.get('group', [])
                if not grp: continue
                print(f'[JyComposeVideo] Track {arg} type={tn}, items={len(grp)}')
                if 'video' in tn: video_tracks.append(list(grp))
                elif 'audio' in tn: audio_tracks.append(list(grp))
                elif 'text' in tn: caption_tracks.append(list(grp))
                elif 'effect' in tn: effect_tracks.append(list(grp))

        total_audio_items = sum(len(t) for t in audio_tracks)
        total_caption_items = sum(len(t) for t in caption_tracks)
        total_effect_items = sum(len(t) for t in effect_tracks)

        all_clips = []
        track_clip_counts = []
        for track_medias in video_tracks:
            track_clips = []
            after_end = 0.0
            for media in track_medias:
                fp = media.get('media_file_full_name', '')
                if not os.path.exists(fp):
                    print(f'[JyComposeVideo] Skip missing: {fp}')
                    continue
                sim = media.get('start_in_media', 0) / 1e6
                sat = media.get('start_at_track', 0) / 1e6
                dur = media.get('duration', 0) / 1e6
                vol = media.get('volume', 1.0)
                anim_datas = media.get('animation_datas', [])
                trans_data = media.get('transition_data', None)

                try:
                    if is_image_file(fp):
                        img = Image.open(fp).convert('RGB')
                        if dur <= 0: dur = 5.0
                        iw, ih = img.size
                        scale_i = min(width / iw, height / ih) if iw > 0 and ih > 0 else 1.0
                        nw_i, nh_i = int(iw * scale_i), int(ih * scale_i)
                        img_rs = img.resize((nw_i, nh_i), Image.LANCZOS)
                        canvas = Image.new('RGB', (width, height), (0, 0, 0))
                        canvas.paste(img_rs, ((width - nw_i) // 2, (height - nh_i) // 2))
                        mc = ImageClip(np.array(canvas), duration=dur).with_fps(fps)
                    else:
                        vc = VideoFileClip(fp)
                        if sim > 0: vc = vc.subclipped(sim)
                        if dur > 0: vc = vc.subclipped(0, min(dur, vc.duration))
                        elif dur <= 0: dur = vc.duration
                        vw, vh = vc.size
                        scale_v = min(width / vw, height / vh) if vw > 0 and vh > 0 else 1.0
                        nw_v, nh_v = int(vw * scale_v), int(vh * scale_v)
                        vc_rs = vc.resized((nw_v, nh_v)).with_fps(fps)
                        bg = ColorClip(size=(width, height), color=(0, 0, 0), duration=vc_rs.duration)
                        if dur <= 0:
                            dur = vc_rs.duration if hasattr(vc_rs, 'duration') and vc_rs.duration else 1.0
                        bg2 = ColorClip(size=(width, height), color=(0, 0, 0), duration=dur)
                        mc = CompositeVideoClip([bg2, vc_rs.with_position(((width - nw_v) // 2, (height - nh_v) // 2))])
                        if vc.audio is not None:
                            mc = mc.with_audio(vc.audio)
                except Exception as e:
                    print(f'[JyComposeVideo] Load error {fp}: {e}')
                    if dur <= 0: dur = 2.0
                    mc = ColorClip(size=(width, height), color=(0, 0, 0), duration=dur).with_fps(fps)

                if sat <= 0: actual_start = after_end
                else: actual_start = sat
                actual_end = actual_start + dur

                # Apply animations via moviepy built-in FX (C-level, no Python per-frame)
                if anim_datas:
                    ac = mc.with_fps(fps)
                    try:
                        for ad in anim_datas:
                            at = ad.get('animation_type', '')
                            an = ad.get('animation', '')
                            adr = max(ad.get('duration', 0) / 1e6, 0.1)
                            if at == 'in':
                                eff = INTRO_ANIMATION_MAP.get(an, 'fade_in')
                                side_in = _SLIDE_IN_MAP.get(eff)
                                if side_in:
                                    ac = ac.with_effects([_vfx.SlideIn(adr, side_in)])
                                elif eff in ('fade_in', 'zoom_in', 'zoom_in_from_small', 'slight_zoom_in', 'dynamic_zoom_in',
                                             'rotate_in', 'rotate_open', 'mirror_flip_in', 'swirl_in',
                                             'fold_open', 'jump_open', 'swing_in_down', 'swing_in_right',
                                             'swing_in_left_up', 'swing_in_right_up', 'swing_in_left_down',
                                             'swing_in_right_down', 'shake', 'shake_v', 'shake_h', 'shake_drop'):
                                    ac = ac.with_effects([_vfx.FadeIn(adr)])
                                else:
                                    ac = ac.with_effects([_vfx.FadeIn(adr)])
                            elif at == 'out':
                                eff = OUTRO_ANIMATION_MAP.get(an, 'fade_out')
                                side_out = _SLIDE_OUT_MAP.get(eff)
                                if side_out:
                                    ac = ac.with_effects([_vfx.SlideOut(adr, side_out)])
                                else:
                                    ac = ac.with_effects([_vfx.FadeOut(adr)])
                    except Exception as e:
                        print(f'[JyComposeVideo] Animation FX failed, using clip as-is: {e}')
                else:
                    ac = mc.with_fps(fps)
                if hasattr(mc, 'audio') and mc.audio:
                    ac.audio = mc.audio.with_volume_scaled(vol) if vol != 1.0 else mc.audio

                trans_info = None
                if trans_data:
                    tn = trans_data.get('transition', '')
                    td = trans_data.get('duration', 0) / 1e6
                    if td <= 0: td = 0.5
                    trans_info = {'type': TRANSITION_MAP.get(tn, 'crossfade'), 'duration': td}

                track_clips.append({'clip': ac, 'start': actual_start, 'end': actual_end,
                              'duration': dur, 'transition': trans_info})
                after_end = actual_end

            # Transitions are handled via crossfade in compositing step (no per-frame overhead)
            all_clips.extend(track_clips)
            track_clip_counts.append(len(track_clips))

        if not all_clips:
            raise Exception('[JyComposeVideo] No valid media clips')
        if width <= 0 or height <= 0:
            raise Exception(f'[JyComposeVideo] Invalid dimensions: {width}x{height}')
        print(f'[JyComposeVideo] Processing: {len(all_clips)} media, {total_audio_items} audio, {total_caption_items} captions, {total_effect_items} effects')
        total_dur = max(c['end'] for c in all_clips)

        # Build per-track videos using concatenate_videoclips (C-level, no Python per-frame)
        # Each track concatenates its clips with crossfade transitions via moviepy built-ins,
        # then multiple tracks are composited together.
        track_videos = []
        clip_idx = 0
        for ti in range(len(track_clip_counts)):
            count = track_clip_counts[ti]
            if count == 0:
                continue
            t_clips = all_clips[clip_idx:clip_idx + count]
            clip_idx += count

            if count == 1:
                track_videos.append(t_clips[0]['clip'])
                continue

            # Build track with crossfade transitions using moviepy built-in effects
            segments = []
            for i, ci in enumerate(t_clips):
                clip = ci['clip']
                trans = ci.get('transition')
                if trans:
                    td = trans['duration']
                    clip = clip.with_effects([_vfx.CrossFadeOut(td)])
                if i > 0:
                    prev_trans = t_clips[i - 1].get('transition')
                    if prev_trans:
                        td = prev_trans['duration']
                        clip = clip.with_effects([_vfx.CrossFadeIn(td)])
                segments.append(clip)

            try:
                track_video = concatenate_videoclips(segments)
            except Exception as e:
                print(f'[JyComposeVideo] Concatenate failed, fallback to composite: {e}')
                elements = []
                pos = 0.0
                for seg in segments:
                    elements.append(seg.with_start(pos))
                    pos += seg.duration
                track_video = CompositeVideoClip(elements, size=(width, height))
            track_videos.append(track_video)

        if len(track_videos) == 0:
            final_video = ColorClip(size=(width, height), color=(0, 0, 0), duration=1).with_fps(fps)
        elif len(track_videos) == 1:
            final_video = track_videos[0]
            print('[JyComposeVideo] Single track, direct concatenation')
        else:
            final_video = CompositeVideoClip(track_videos, size=(width, height))
            print(f'[JyComposeVideo] {len(track_videos)} tracks composited')

        if total_dur > 0:
            final_video = final_video.with_duration(total_dur)

        # Subtitles
        if total_caption_items > 0:
            cap_elements = []
            for track_captions in caption_tracks:
                ac_end = 0.0
                for cap in track_captions:
                    text = cap.get('subtitle', '')
                    fn = cap.get('font', '????')
                    col = cap.get('color', '#FFFFFF')
                    sz = cap.get('size', 8.0)
                    sat = cap.get('start_at_track', 0) / 1e6
                    cd = cap.get('duration', 0) / 1e6
                    cs = cap.get('clip_settings', {})
                    tx = cs.get('transform_x', 0.0)
                    ty = cs.get('transform_y', -0.8)
                    if cd <= 0: cd = 2.0
                    if sat <= 0: sat = ac_end
                    try:
                        rgba = render_subtitle(text, fn, sz, col, width, height, tx, ty)
                        rgb_img = rgba[:, :, :3]
                        alpha_img = rgba[:, :, 3].astype(float) / 255.0
                        sub_clip = ImageClip(rgb_img, duration=cd).with_start(sat).with_fps(fps)
                        mask = ImageClip(alpha_img, is_mask=True, duration=cd).with_start(sat)
                        sub_clip = sub_clip.with_mask(mask)
                        cap_elements.append(sub_clip)
                    except Exception as e:
                        print(f'[JyComposeVideo] Subtitle error: {e}')
                    ac_end = sat + cd
            print(f'[JyComposeVideo] Rendered {len(cap_elements)}/{total_caption_items} subtitles')
            if cap_elements:
                final_video = CompositeVideoClip([final_video] + cap_elements, size=(width, height))
                if total_dur > 0:
                    final_video = final_video.with_duration(total_dur)

        # Audio
        audio_clips = []
        for track_audios in audio_tracks:
            aa_end = 0.0
            for aud in track_audios:
                afp = aud.get('media_file_full_name', '')
                if not afp or not os.path.exists(afp):
                    print(f'[JyComposeVideo] Audio file missing: {afp}')
                    continue
                sim_s = aud.get('start_in_media', 0) / 1e6
                sat_s = aud.get('start_at_track', 0) / 1e6
                adur_s = aud.get('duration', 0) / 1e6
                avol = aud.get('volume', 1.0)
                try:
                    ac = AudioFileClip(afp)
                    if sim_s > 0: ac = ac.subclipped(sim_s)
                    if adur_s > 0: ac = ac.subclipped(0, min(adur_s, ac.duration))
                    if avol != 1.0: ac = ac.with_volume_scaled(avol)
                    if sat_s <= 0: sat_s = aa_end
                    ac = ac.with_start(sat_s)
                    audio_clips.append(ac)
                    aa_end = sat_s + ac.duration
                except Exception as e:
                    print(f'[JyComposeVideo] Audio error {afp}: {e}')

        print(f'[JyComposeVideo] Audio loaded: {len(audio_clips)}/{total_audio_items}')
        if audio_clips:
            try:
                final_video = final_video.with_audio(CompositeAudioClip(audio_clips))
                print(f'[JyComposeVideo] Audio composited: {len(audio_clips)} clips')
            except Exception as e:
                print(f'[JyComposeVideo] Audio composite failed: {e}')

        # Effects via moviepy built-in FX (C-level, no Python per-frame)
        applied_count = 0
        for track_effects in effect_tracks:
            for eff in track_effects:
                ename = eff.get("effect_name_or_resource_id", "")
                if not ename:
                    continue
                eff_key = EFFECT_MAP.get(ename)
                if not eff_key:
                    for k in EFFECT_MAP:
                        if k in ename or ename.lower() in k.lower():
                            eff_key = EFFECT_MAP[k]
                            break
                if not eff_key:
                    print(f"[JyComposeVideo] Effect not supported, skipped: {ename}")
                    continue
                try:
                    if eff_key == 'grayscale':
                        final_video = final_video.with_effects([_vfx.BlackAndWhite()])
                    elif eff_key == 'invert':
                        final_video = final_video.with_effects([_vfx.InvertColors()])
                    elif eff_key == 'brighten':
                        final_video = final_video.with_effects([_vfx.LumContrast(lum=1.3, contrast=1.0)])
                    elif eff_key == 'darken':
                        final_video = final_video.with_effects([_vfx.LumContrast(lum=0.7, contrast=1.0)])
                    elif eff_key == 'warm':
                        final_video = final_video.with_effects([_vfx.MultiplyColor(1.1)])
                    elif eff_key == 'cool':
                        final_video = final_video.with_effects([_vfx.MultiplyColor(0.9)])
                    elif eff_key == 'mirror_h':
                        final_video = final_video.with_effects([_vfx.MirrorX()])
                    elif eff_key == 'mirror_v':
                        final_video = final_video.with_effects([_vfx.MirrorY()])
                    else:
                        print(f"[JyComposeVideo] Effect {ename} requires Python frame processing, skipped for speed")
                        continue
                    applied_count += 1
                except Exception as e:
                    print(f"[JyComposeVideo] Effect {ename} failed: {e}")

        if applied_count > 0:
            print(f"[JyComposeVideo] Applied {applied_count}/{total_effect_items} effects via moviepy FX")


        # Export ? detect GPU encoders for hardware acceleration
        import subprocess
        hw_encoder = None
        try:
            result = subprocess.run(['ffmpeg', '-hide_banner', '-encoders'],
                                    capture_output=True, text=True, timeout=5,
                                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
            if 'h264_nvenc' in result.stdout:
                hw_encoder = 'h264_nvenc'
            elif 'h264_qsv' in result.stdout:
                hw_encoder = 'h264_qsv'
            elif 'h264_amf' in result.stdout:
                hw_encoder = 'h264_amf'
        except Exception as e:
            print(f'[JyComposeVideo] GPU detection skipped: {e}')

        output_filename = f'{draft_name}_{uuid.uuid4().hex[:8]}.mp4'
        output_path = os.path.join(self.output_dir, output_filename)

        has_audio = final_video.audio is not None if hasattr(final_video, 'audio') else False
        print(f'[JyComposeVideo] Final: size={final_video.size}, dur={final_video.duration:.1f}s, audio={"yes" if has_audio else "no"}')

        fv_size = final_video.size if hasattr(final_video, 'size') else (0, 0)
        if fv_size[0] <= 0 or fv_size[1] <= 0:
            raise Exception(f'[JyComposeVideo] Invalid output size: {fv_size}, input was {width}x{height}')

        # Build export attempts: GPU first, then software fallback
        export_attempts = []
        if hw_encoder:
            hw_preset_map = {'h264_nvenc': 'p4', 'h264_amf': 'speed', 'h264_qsv': 'veryfast'}
            hw_preset = hw_preset_map.get(hw_encoder, 'medium')
            export_attempts.append({
                'codec': hw_encoder, 'audio_codec': 'aac', '_preset': hw_preset,
                '_label': f'GPU ({hw_encoder})'
            })
            print(f'[JyComposeVideo] Hardware encoder detected: {hw_encoder}')
        export_attempts.extend([
            {'codec': 'libx264', 'audio_codec': 'aac', '_label': 'CPU (x264 + aac)'},
            {'codec': 'libx264', 'audio_codec': 'libmp3lame', '_label': 'CPU (x264 + mp3)'},
            {'codec': 'libx264', 'audio': False, '_label': 'CPU (x264, no audio)'},
        ])

        export_ok = False
        for attempt in export_attempts:
            try:
                apreset = attempt.pop('_preset', 'veryfast')
                label = attempt.pop('_label', '')
                final_video.write_videofile(output_path, fps=fps, preset=apreset,
                                            threads=max(4, os.cpu_count() or 4), logger='bar', **attempt)
                export_ok = True
                print(f'[JyComposeVideo] Export OK via {label}')
                break
            except Exception as e:
                print(f'[JyComposeVideo] Export via {label} failed: {e}')
        if not export_ok:
            raise Exception('[JyComposeVideo] All export attempts failed')

        for ci in all_clips:
            try: ci['clip'].close()
            except: pass
        for ac in audio_clips:
            try: ac.close()
            except: pass
        try: final_video.close()
        except: pass

        results = [{'filename': output_filename, 'subfolder': '', 'type': self.type}]
        return { "ui": { "images": results, "animated": (True,) },"result": (output_path, total_dur) }
    
class JyComposeVideoOut(JyComposeVideo):
    OUTPUT_NODE = True


NODE_CLASS_MAPPINGS = {
    'JyComposeVideo': JyComposeVideo,
    'JyComposeVideoOut':JyComposeVideoOut
}

NODE_DISPLAY_NAME_MAPPINGS = {
    'JyComposeVideo': '剪映合成视频非输出',
    'JyComposeVideoOut': '剪映合成视频'
}

import os, sys, time, urllib.request, json
from seleniumbase import SB

# ==========================================
# 💡 核心配置 (适配全新 g4f.gg 界面)
# ==========================================
TARGET_URL = "https://g4f.gg/renqi" 
MC_USERNAME = "renqi"

TG_TOKEN = os.getenv("TG_TOKEN", "")
TG_CHAT = os.getenv("TG_CHAT_ID", "")

def send_tg(msg):
    if TG_TOKEN and TG_CHAT:
        try:
            url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
            data = json.dumps({"chat_id": TG_CHAT, "text": f"🤖 G4F 自动续期:\n{msg}"}).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req, timeout=10)
        except:
            pass

print(f"\n===== 🚀 开始执行极速续期 (G4F.GG 赛博朋克全新版) =====")

proxy_str = "socks5://127.0.0.1:40000"

with SB(uc=True, proxy=proxy_str, headless=False) as sb:
    try:
        print(f"🌐 正在通过 WARP 访问新版目标网址: {TARGET_URL}")
        sb.open(TARGET_URL)
        
        # 给炫酷的 UI 一点加载时间
        sb.sleep(6) 
        
        os.makedirs("screenshots", exist_ok=True)
        sb.save_screenshot("screenshots/1_page_loaded.png")

        print("✍️ 尝试填入游戏ID (OPTIONAL)...")
        try:
            # 扩大搜索范围，防止 placeholder 变动
            sb.type('input[placeholder*="Steve"], input[placeholder*="Player"]', MC_USERNAME, timeout=5)
            print("✅ ID 填入成功！")
        except:
            print("ℹ️ 未找到输入框或无需填入，继续下一步。")

        print("🚀 寻找 [+ ADD 90 MIN] 核心按钮并执行降维打击...")
        
        # 🌟 核心杀手锏：注入原生 JavaScript 寻找并强制点击！
        # 无视任何 HTML 标签、大小写、图层遮挡，直接在浏览器渲染层找出包含 "ADD 90" 的最深层元素并扣动扳机！
        js_click_code = """
        let clicked = false;
        // 获取页面上所有可能的点击载体
        let els = document.querySelectorAll('button, a, input, div, span');
        // 倒序遍历（确保先碰到最内层的子元素，避免误点到外层的无用大容器）
        for (let i = els.length - 1; i >= 0; i--) {
            let el = els[i];
            // 提取元素表面的文本或 value，并统统强制转为大写
            let text = (el.innerText || el.value || '').toUpperCase();
            // 只要文字里包含 ADD 90，管它底层是什么，直接按死！
            if (text.includes('ADD 90')) {
                el.click();
                clicked = true;
                break;
            }
        }
        return clicked;
        """
        
        # 执行这段神级 JS 代码
        is_clicked = sb.execute_script(js_click_code)
        
        if is_clicked:
            print("🖱️ JavaScript 强制穿透点击成功！")
        else:
            print("⚠️ JS 未能点击，尝试备用纯正 XPath 方案...")
            # 备用方案：严格声明 xpath=，并且使用 translate 忽略大小写
            sb.click('xpath=//*[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "add 90")]')

        print("⏳ 等待服务器处理续期请求...")
        # 点击后多等一会儿，确保结果出来
        sb.sleep(8)
        sb.save_screenshot("screenshots/2_result.png")

        print("✅ 续期点击已执行！")
        send_tg(f"✅ 服务器 [{MC_USERNAME}] 续期按钮已成功点击！\n官方界面已重构，请查阅 GitHub 截图确认是否成功增加了 90 分钟。")

    except Exception as e:
        print(f"❌ 发生致命错误: {e}")
        os.makedirs("screenshots", exist_ok=True)
        sb.save_screenshot("screenshots/error.png")
        send_tg(f"❌ 自动续期崩溃: {e}")

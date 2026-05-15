# File này chứa toàn bộ mã nguồn máy chủ web và giao diện Portfolio chuyên nghiệp của bạn.
# Phiên bản NÂNG CẤP với nhiều hiệu ứng đẹp mắt
# Không cần cài thêm thư viện - All from CDN!

from flask import Flask, render_template_string

# Khởi tạo đối tượng ứng dụng Flask, đóng vai trò điều phối toàn bộ máy chủ web.
app = Flask(__name__)

# Biến này lưu trữ toàn bộ cấu trúc HTML, CSS, và JavaScript của trang web.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Duong Duy Khang | Professional Portfolio</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        /* Khai báo các biến màu sắc dùng chung cho toàn bộ trang web để dễ dàng thay đổi tone màu */
        :root {
            --bg-primary: #0a0e27;
            --bg-secondary: #1a1f3a;
            --bg-card: #252b48;
            --accent-cyan: #00d9ff;
            --accent-purple: #a78bfa;
            --accent-pink: #ec4899;
            --text-primary: #ffffff;
            --text-secondary: #94a3b8;
            --glow-cyan: rgba(0, 217, 255, 0.5);
            --glow-purple: rgba(167, 139, 250, 0.5);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
            scroll-behavior: smooth;
            cursor: none;
        }

        /* ===== LOADING SCREEN ===== */
        .loading-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--bg-primary);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            transition: opacity 0.5s ease, visibility 0.5s ease;
        }

        .loading-screen.hide {
            opacity: 0;
            visibility: hidden;
        }

        .loader {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(0, 217, 255, 0.2);
            border-top: 4px solid var(--accent-cyan);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 1.5rem;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .loading-text {
            color: var(--accent-cyan);
            font-size: 1.2rem;
            font-weight: 600;
            animation: pulse 1.5s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* ===== CUSTOM CURSOR ===== */
        .cursor {
            width: 20px;
            height: 20px;
            border: 2px solid var(--accent-cyan);
            border-radius: 50%;
            position: fixed;
            pointer-events: none;
            z-index: 9999;
            transition: all 0.1s ease;
            transform: translate(-50%, -50%);
        }

        .cursor-follower {
            width: 40px;
            height: 40px;
            border: 1px solid rgba(0, 217, 255, 0.3);
            border-radius: 50%;
            position: fixed;
            pointer-events: none;
            z-index: 9998;
            transition: all 0.3s ease;
            transform: translate(-50%, -50%);
        }

        /* ===== ANIMATED BACKGROUND GRADIENTS ===== */
        .animated-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            opacity: 0.3;
            overflow: hidden;
        }

        .gradient-ball {
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            animation: float 20s infinite ease-in-out;
        }

        .ball-1 {
            width: 500px;
            height: 500px;
            background: var(--accent-cyan);
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }

        .ball-2 {
            width: 400px;
            height: 400px;
            background: var(--accent-purple);
            bottom: 10%;
            right: 10%;
            animation-delay: 3s;
        }

        .ball-3 {
            width: 450px;
            height: 450px;
            background: var(--accent-pink);
            top: 50%;
            left: 50%;
            animation-delay: 6s;
        }

        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            25% { transform: translate(100px, -100px) scale(1.1); }
            50% { transform: translate(-80px, 80px) scale(0.9); }
            75% { transform: translate(80px, 120px) scale(1.05); }
        }

        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: 0;
            opacity: 0.6;
        }

        nav {
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            background: rgba(10, 14, 39, 0.8);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding: 1rem 0;
            transition: all 0.3s ease;
        }

        nav.scrolled {
            padding: 0.7rem 0;
            background: rgba(10, 14, 39, 0.95);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }

        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 3rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: 900;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 2px;
            animation: glow 2s ease-in-out infinite;
        }

        @keyframes glow {
            0%, 100% { filter: drop-shadow(0 0 5px var(--accent-cyan)); }
            50% { filter: drop-shadow(0 0 15px var(--accent-cyan)); }
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2.5rem;
        }

        .nav-links a {
            color: var(--text-secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
            padding: 0.5rem 0;
        }

        .nav-links a::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
            transition: width 0.3s ease;
        }

        .nav-links a:hover {
            color: var(--accent-cyan);
        }

        .nav-links a:hover::after {
            width: 100%;
        }

        .menu-toggle {
            display: none;
            flex-direction: column;
            cursor: pointer;
            gap: 5px;
        }

        .menu-toggle span {
            width: 25px;
            height: 3px;
            background: var(--accent-cyan);
            transition: all 0.3s ease;
            border-radius: 2px;
        }

        .hero {
            position: relative;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 3rem;
            overflow: hidden;
        }

        .hero-content {
            position: relative;
            z-index: 1;
            text-align: center;
            max-width: 900px;
        }

        .hero-tag {
            display: inline-block;
            padding: 0.5rem 1.5rem;
            background: rgba(0, 217, 255, 0.1);
            border: 1px solid var(--accent-cyan);
            border-radius: 50px;
            color: var(--accent-cyan);
            font-size: 0.9rem;
            margin-bottom: 2rem;
            animation: fadeInDown 0.8s ease;
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.2);
        }

        /* ===== TYPING EFFECT ===== */
        .typing-container {
            min-height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
        }

        .typing-text {
            font-size: clamp(3rem, 8vw, 5.5rem);
            font-weight: 900;
            line-height: 1.1;
        }

        .typing-text span {
            background: linear-gradient(135deg, #fff, var(--accent-cyan), var(--accent-purple));
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientShift 3s ease infinite;
        }

        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .cursor-blink {
            display: inline-block;
            width: 4px;
            height: 1em;
            background: var(--accent-cyan);
            animation: blink 0.7s infinite;
            margin-left: 5px;
            vertical-align: middle;
        }

        @keyframes blink {
            0%, 49% { opacity: 1; }
            50%, 100% { opacity: 0; }
        }

        .hero-subtitle {
            font-size: clamp(1.1rem, 2vw, 1.4rem);
            color: var(--text-secondary);
            margin-bottom: 3rem;
            line-height: 1.8;
            animation: fadeInUp 0.8s ease 0.4s both;
        }

        .cta-buttons {
            display: flex;
            gap: 1.5rem;
            justify-content: center;
            flex-wrap: wrap;
            animation: fadeInUp 0.8s ease 0.6s both;
        }

        .btn {
            padding: 1rem 2.5rem;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.5s ease, height 0.5s ease;
        }

        .btn:hover::before {
            width: 300px;
            height: 300px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            color: white;
            box-shadow: 0 10px 30px var(--glow-cyan);
        }

        .btn-primary:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px var(--glow-cyan);
        }

        .btn-outline {
            border: 2px solid var(--accent-cyan);
            color: var(--accent-cyan);
            background: transparent;
        }

        .btn-outline:hover {
            background: var(--accent-cyan);
            color: var(--bg-primary);
            transform: translateY(-5px);
        }

        /* ===== FLOATING SHAPES ===== */
        .floating-shapes {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            pointer-events: none;
        }

        .shape {
            position: absolute;
            opacity: 0.08;
            animation: floatShape 15s infinite ease-in-out;
        }

        .shape-1 {
            top: 15%;
            left: 10%;
            font-size: 80px;
            animation-delay: 0s;
        }

        .shape-2 {
            top: 60%;
            right: 10%;
            font-size: 100px;
            animation-delay: 3s;
        }

        .shape-3 {
            bottom: 20%;
            left: 50%;
            font-size: 90px;
            animation-delay: 6s;
        }

        @keyframes floatShape {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-50px) rotate(180deg); }
        }

        section {
            position: relative;
            z-index: 1;
            padding: 8rem 3rem;
            max-width: 1400px;
            margin: 0 auto;
        }

        .section-header {
            text-align: center;
            margin-bottom: 5rem;
        }

        .section-tag {
            display: inline-block;
            color: var(--accent-cyan);
            font-size: 0.95rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 1rem;
            position: relative;
        }

        .section-tag::before,
        .section-tag::after {
            content: '';
            position: absolute;
            top: 50%;
            width: 40px;
            height: 2px;
            background: var(--accent-cyan);
        }

        .section-tag::before { left: -50px; }
        .section-tag::after { right: -50px; }

        .section-title {
            font-size: clamp(2.5rem, 5vw, 3.5rem);
            font-weight: 900;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--text-primary), var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .section-subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
            max-width: 600px;
            margin: 0 auto;
        }

        .about-grid {
            display: grid;
            grid-template-columns: 1fr 1.5fr;
            gap: 5rem;
            align-items: center;
        }

        .profile-image-container {
            position: relative;
        }

        .profile-image {
            width: 100%;
            max-width: 400px;
            aspect-ratio: 1;
            border-radius: 30px;
            object-fit: cover;
            position: relative;
            z-index: 2;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
            transition: transform 0.3s ease;
        }

        .profile-image:hover {
            transform: scale(1.05) rotate(2deg);
        }

        .profile-image-container::before {
            content: '';
            position: absolute;
            top: -20px;
            left: -20px;
            right: 20px;
            bottom: 20px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            border-radius: 30px;
            z-index: 1;
            opacity: 0.3;
            animation: rotateBorder 10s linear infinite;
        }

        @keyframes rotateBorder {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .about-content {
            padding: 2rem;
        }

        .about-content h3 {
            font-size: 2rem;
            margin-bottom: 1.5rem;
            color: var(--accent-cyan);
        }

        .about-content p {
            color: var(--text-secondary);
            font-size: 1.1rem;
            line-height: 1.8;
            margin-bottom: 2rem;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            margin-top: 3rem;
        }

        .stat-item {
            text-align: center;
            padding: 1.5rem;
            background: var(--bg-card);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .stat-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 217, 255, 0.1), transparent);
            transition: left 0.5s ease;
        }

        .stat-item:hover::before {
            left: 100%;
        }

        .stat-item:hover {
            transform: translateY(-5px);
            border-color: var(--accent-cyan);
            box-shadow: 0 10px 30px rgba(0, 217, 255, 0.2);
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: block;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 2rem;
            align-items: stretch;
        }

        /* ===== 3D TILT CARDS ===== */
        .skill-card {
            background: var(--bg-card);
            padding: 2.5rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 100%;
            transform-style: preserve-3d;
            will-change: transform;
        }

        .skill-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .skill-card:hover::before {
            transform: scaleX(1);
        }

        .skill-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            opacity: 0;
            border-radius: 20px;
            transition: opacity 0.3s ease;
            z-index: -1;
            filter: blur(20px);
        }

        .skill-card:hover::after {
            opacity: 0.2;
        }

        .skill-card:hover {
            transform: translateY(-10px);
            border-color: var(--accent-cyan);
            box-shadow: 0 20px 40px rgba(0, 217, 255, 0.3);
        }

        .skill-icon {
            font-size: 3rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .skill-card h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }

        .skill-card p {
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 1.5rem;
            flex-grow: 1;
        }

        .skill-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .skill-tag {
            padding: 0.4rem 1rem;
            background: rgba(0, 217, 255, 0.1);
            border: 1px solid rgba(0, 217, 255, 0.3);
            border-radius: 20px;
            font-size: 0.85rem;
            color: var(--accent-cyan);
            transition: all 0.3s ease;
        }

        .skill-tag:hover {
            background: rgba(0, 217, 255, 0.2);
            transform: translateY(-2px);
        }

        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 3rem;
        }

        .project-card {
            background: var(--bg-card);
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.4s ease;
            position: relative;
        }

        .project-card:hover {
            transform: translateY(-15px) scale(1.02);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
        }

        .project-image-wrapper {
            position: relative;
            overflow: hidden;
            height: 250px;
        }

        .project-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }

        .project-card:hover .project-image {
            transform: scale(1.2) rotate(2deg);
        }

        .project-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.8));
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .project-card:hover .project-overlay {
            opacity: 1;
        }

        .project-content {
            padding: 2rem;
        }

        .project-badge {
            display: inline-block;
            padding: 0.3rem 1rem;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }

        .project-content h3 {
            font-size: 1.8rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }

        .project-content p {
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }

        .project-links {
            display: flex;
            gap: 1rem;
        }

        .project-link {
            padding: 0.7rem 1.5rem;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .project-link-primary {
            background: var(--accent-cyan);
            color: var(--bg-primary);
        }

        .project-link-primary:hover {
            background: var(--accent-purple);
            transform: translateX(5px);
        }

        .project-link-secondary {
            border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan);
        }

        .project-link-secondary:hover {
            background: var(--accent-cyan);
            color: var(--bg-primary);
        }

        .contact-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 5rem;
            align-items: center;
        }

        .contact-info h3 {
            font-size: 2.5rem;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .contact-methods {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .contact-item {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            padding: 1.5rem;
            background: var(--bg-card);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }

        .contact-item:hover {
            border-color: var(--accent-cyan);
            transform: translateX(10px);
            box-shadow: 0 10px 30px rgba(0, 217, 255, 0.2);
        }

        .contact-icon {
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            border-radius: 50%;
            font-size: 1.3rem;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(0, 217, 255, 0.7); }
            50% { box-shadow: 0 0 0 15px rgba(0, 217, 255, 0); }
        }

        .contact-details h4 {
            font-size: 1rem;
            color: var(--text-secondary);
            margin-bottom: 0.3rem;
        }

        .contact-details p {
            font-size: 1.1rem;
            color: var(--text-primary);
        }

        .contact-details a {
            color: var(--accent-cyan);
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .contact-details a:hover {
            color: var(--accent-purple);
        }

        .social-links {
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
        }

        .social-link {
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-card);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            color: var(--accent-cyan);
            font-size: 1.3rem;
            transition: all 0.3s ease;
            text-decoration: none;
        }

        .social-link:hover {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            color: white;
            transform: translateY(-5px) rotate(360deg);
        }

        /* Định dạng riêng cho khối hiển thị mã QR */
        .qr-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: var(--bg-card);
            padding: 3rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            text-align: center;
            transition: all 0.3s ease;
        }

        .qr-section:hover {
            border-color: var(--accent-cyan);
            box-shadow: 0 15px 40px rgba(0, 217, 255, 0.2);
            transform: scale(1.05);
        }

        .qr-section h3 {
            font-size: 1.8rem;
            color: var(--text-primary);
            margin-bottom: 1.5rem;
        }

        .qr-container {
            background: white;
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 1.5rem;
            display: inline-block;
            box-shadow: 0 10px 30px var(--glow-cyan);
            transition: all 0.3s ease;
        }

        .qr-container:hover {
            transform: rotate(5deg) scale(1.1);
        }

        .qr-image {
            width: 200px;
            height: 200px;
            object-fit: contain;
        }

        .qr-section p {
            color: var(--text-secondary);
            font-size: 1rem;
        }

        footer {
            text-align: center;
            padding: 3rem;
            background: var(--bg-secondary);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-secondary);
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 1200px) {
            .skills-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 968px) {
            body { cursor: auto; }
            .cursor, .cursor-follower { display: none; }
            
            .nav-links {
                position: fixed;
                left: -100%;
                top: 70px;
                flex-direction: column;
                background: var(--bg-secondary);
                width: 100%;
                text-align: center;
                transition: 0.3s;
                padding: 2rem;
                gap: 1.5rem;
            }

            .nav-links.active { left: 0; }
            .menu-toggle { display: flex; }
            .about-grid, .contact-grid { grid-template-columns: 1fr; gap: 3rem; }
            .projects-grid, .stats-grid { grid-template-columns: 1fr; }
            section { padding: 5rem 1.5rem; }
            .hero { padding: 0 1.5rem; }
            .cta-buttons { flex-direction: column; }
            .section-tag::before, .section-tag::after { display: none; }
        }

        @media (max-width: 768px) {
            .skills-grid {
                grid-template-columns: 1fr;
            }
        }

        .reveal {
            opacity: 0;
            transform: translateY(50px);
            transition: all 0.8s ease;
        }

        .reveal.active {
            opacity: 1;
            transform: translateY(0);
        }
    </style>
</head>
<body>

    <!-- Loading Screen -->
    <div class="loading-screen" id="loadingScreen">
        <div class="loader"></div>
        <div class="loading-text">Loading Portfolio...</div>
    </div>

    <!-- Custom Cursor -->
    <div class="cursor"></div>
    <div class="cursor-follower"></div>

    <!-- Animated Background -->
    <div class="animated-bg">
        <div class="gradient-ball ball-1"></div>
        <div class="gradient-ball ball-2"></div>
        <div class="gradient-ball ball-3"></div>
    </div>

    <!-- Particles Background -->
    <div id="particles-js"></div>

    <nav id="navbar">
        <div class="nav-container">
            <div class="logo">D.D.KHANG</div>
            <ul class="nav-links" id="navLinks">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#skills">Skills</a></li>
                <li><a href="#projects">Projects</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
            <div class="menu-toggle" id="menuToggle">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </nav>

    <section id="home" class="hero">
        <!-- Floating Shapes -->
        <div class="floating-shapes">
            <i class="fas fa-code shape shape-1"></i>
            <i class="fas fa-laptop-code shape shape-2"></i>
            <i class="fas fa-terminal shape shape-3"></i>
        </div>

        <div class="hero-content">
            <div class="hero-tag">
                <i class="fas fa-rocket"></i> Welcome to my portfolio
            </div>
            
            <!-- Typing Effect Container -->
            <div class="typing-container">
                <div class="typing-text">
                    <span id="typingText"></span>
                    <span class="cursor-blink"></span>
                </div>
            </div>
            
            <p class="hero-subtitle">
                A passionate IT student crafting innovative digital solutions with clean code and modern design principles. 
                Transforming ideas into impactful user experiences.
            </p>
            <div class="cta-buttons">
                <a href="#projects" class="btn btn-primary">
                    View My Work <i class="fas fa-arrow-right"></i>
                </a>
                <a href="#contact" class="btn btn-outline">
                    Get In Touch <i class="fas fa-envelope"></i>
                </a>
            </div>
        </div>
    </section>

    <section id="about">
        <div class="section-header reveal">
            <div class="section-tag">About Me</div>
            <h2 class="section-title">Who I Am</h2>
            <p class="section-subtitle">
                Passionate about technology and driven by innovation
            </p>
        </div>
        <div class="about-grid reveal">
            <div class="profile-image-container">
                <img src="/static/profile.jpg" alt="Duong Duy Khang" class="profile-image">
            </div>
            <div class="about-content">
                <h3>Building the Future, One Line at a Time</h3>
                <p>
                    I'm Duong Duy Khang, a fourth-year Information Technology student at Nam Can Tho University. 
                    My journey in tech is driven by a deep passion for creating meaningful digital experiences 
                    that solve real-world problems.
                </p>
                <p>
                    I specialize in full-stack development with a keen eye for design and user experience. 
                    My approach combines technical expertise with creative thinking to deliver solutions 
                    that are both functional and beautiful.
                </p>
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-number">4+</span>
                        <span class="stat-label">Years Experience</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">10+</span>
                        <span class="stat-label">Projects Done</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">100%</span>
                        <span class="stat-label">Client Satisfied</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="skills">
        <div class="section-header reveal">
            <div class="section-tag">My Expertise</div>
            <h2 class="section-title">Skills & Technologies</h2>
            <p class="section-subtitle">
                Constantly learning and adapting to new technologies
            </p>
        </div>
        <div class="skills-grid">
            <div class="skill-card reveal card-3d">
                <i class="fas fa-code skill-icon"></i>
                <h3>Backend Development</h3>
                <p>Building robust and scalable server-side applications with modern frameworks and best practices.</p>
                <div class="skill-tags">
                    <span class="skill-tag">Python</span>
                    <span class="skill-tag">Flask</span>
                    <span class="skill-tag">REST API</span>
                    <span class="skill-tag">Database</span>
                </div>
            </div>
            <div class="skill-card reveal card-3d">
                <i class="fas fa-palette skill-icon"></i>
                <h3>Frontend Development</h3>
                <p>Creating beautiful, responsive interfaces with attention to detail and user experience.</p>
                <div class="skill-tags">
                    <span class="skill-tag">HTML5</span>
                    <span class="skill-tag">CSS3</span>
                    <span class="skill-tag">JavaScript</span>
                    <span class="skill-tag">Responsive</span>
                </div>
            </div>
            <div class="skill-card reveal card-3d">
                <i class="fas fa-tools skill-icon"></i>
                <h3>Tools & Technologies</h3>
                <p>Utilizing modern development tools and methodologies for efficient workflow.</p>
                <div class="skill-tags">
                    <span class="skill-tag">Git</span>
                    <span class="skill-tag">SQL</span>
                    <span class="skill-tag">Testing</span>
                    <span class="skill-tag">AI-Assisted Coding</span>
                    <span class="skill-tag">Prompt Engineering</span>
                    <span class="skill-tag">DevOps</span>
                </div>
            </div>
            <div class="skill-card reveal card-3d">
                <i class="fas fa-lightbulb skill-icon"></i>
                <h3>Soft Skills</h3>
                <p>Strong communication and collaboration abilities for effective teamwork.</p>
                <div class="skill-tags">
                    <span class="skill-tag">Teamwork</span>
                    <span class="skill-tag">Problem Solving</span>
                    <span class="skill-tag">Creativity</span>
                    <span class="skill-tag">Adaptability</span>
                </div>
            </div>
        </div>
    </section>

    <section id="projects">
        <div class="section-header reveal">
            <div class="section-tag">My Work</div>
            <h2 class="section-title">Featured Projects</h2>
            <p class="section-subtitle">
                A showcase of my recent work and achievements
            </p>
        </div>
        <div class="projects-grid">
            <div class="project-card reveal">
                <div class="project-image-wrapper">
                    <img src="/static/motoworld.jpg" alt="Moto World" class="project-image">
                    <div class="project-overlay"></div>
                </div>
                <div class="project-content">
                    <span class="project-badge">Web Application</span>
                    <h3>Moto World Website</h3>
                    <p>
                        A comprehensive motorcycle showroom platform featuring an AI-powered chatbot for customer support 
                        and an advanced banner management system for dynamic content updates.
                    </p>
                    <div class="project-links">
                        <a href="https://moto-world.vercel.app" target="_blank" class="project-link project-link-primary">
                            Live Demo <i class="fas fa-external-link-alt"></i>
                        </a>
                        <a href="https://github.com/d2khang/moto-world" target="_blank" class="project-link project-link-secondary">
                            <i class="fab fa-github"></i> Code
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="contact">
        <div class="section-header reveal">
            <div class="section-tag">Get In Touch</div>
            <h2 class="section-title">Let's Work Together</h2>
            <p class="section-subtitle">
                Have a project in mind? Let's create something amazing!
            </p>
        </div>
        <div class="contact-grid reveal">
            <div class="contact-info">
                <h3>Ready to Start?</h3>
                <div class="contact-methods">
                    <div class="contact-item">
                        <div class="contact-icon">
                            <i class="fas fa-envelope"></i>
                        </div>
                        <div class="contact-details">
                            <h4>Email</h4>
                            <p><a href="mailto:ddkhang11102004@gmail.com">ddkhang11102004@gmail.com</a></p>
                        </div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">
                            <i class="fas fa-phone"></i>
                        </div>
                        <div class="contact-details">
                            <h4>Phone</h4>
                            <p><a href="tel:0914708593">0914 708 593</a></p>
                        </div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">
                            <i class="fas fa-map-marker-alt"></i>
                        </div>
                        <div class="contact-details">
                            <h4>Location</h4>
                            <p>Can Tho City, Vietnam</p>
                        </div>
                    </div>
                </div>
                <div class="social-links">
                    <a href="https://github.com/d2khang" target="_blank" class="social-link">
                        <i class="fab fa-github"></i>
                    </a>
                    <a href="https://www.facebook.com/duong.khang.50364592/" target="_blank" class="social-link">
                        <i class="fab fa-facebook"></i>
                    </a>
                </div>
            </div>
            
            <div class="qr-section">
                <h3>Scan to Connect</h3>
                <div class="qr-container">
                    <img src="/static/qrcode.png" alt="QR Profile" class="qr-image">
                </div>
                <p>Scan this QR code to quickly view my profile or add me to your contacts.</p>
            </div>
        </div>
    </section>

    <footer>
        <p>&copy; 2026 Duong Duy Khang. All rights reserved. Built with passion and <span style="color: var(--accent-pink);">❤</span></p>
    </footer>

    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        // ===== LOADING SCREEN =====
        window.addEventListener('load', () => {
            setTimeout(() => {
                document.getElementById('loadingScreen').classList.add('hide');
            }, 1500);
        });

        // ===== CUSTOM CURSOR =====
        const cursor = document.querySelector('.cursor');
        const follower = document.querySelector('.cursor-follower');

        if (window.innerWidth > 768) {
            document.addEventListener('mousemove', (e) => {
                cursor.style.left = e.clientX + 'px';
                cursor.style.top = e.clientY + 'px';
                
                setTimeout(() => {
                    follower.style.left = e.clientX + 'px';
                    follower.style.top = e.clientY + 'px';
                }, 100);
            });
        }

        // ===== TYPING EFFECT =====
        const texts = [
            "Hi, I'm Duong Duy Khang",
            "Full Stack Developer",
            "UI/UX Enthusiast",
            "Problem Solver"
        ];
        let textIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        const typingElement = document.getElementById('typingText');

        function typeEffect() {
            const currentText = texts[textIndex];
            
            if (isDeleting) {
                typingElement.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
            } else {
                typingElement.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
            }

            let speed = isDeleting ? 50 : 100;

            if (!isDeleting && charIndex === currentText.length) {
                speed = 2000;
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                textIndex = (textIndex + 1) % texts.length;
                speed = 500;
            }

            setTimeout(typeEffect, speed);
        }

        typeEffect();

        // ===== PARTICLES =====
        particlesJS('particles-js', {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: '#00d9ff' },
                shape: { type: 'circle' },
                opacity: { value: 0.3, random: true },
                size: { value: 3, random: true },
                line_linked: { enable: true, distance: 150, color: '#00d9ff', opacity: 0.2, width: 1 },
                move: { enable: true, speed: 2, random: true }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: { enable: true, mode: 'grab' },
                    onclick: { enable: true, mode: 'push' }
                }
            }
        });

        // ===== NAVBAR SCROLL =====
        const navbar = document.getElementById('navbar');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // ===== MOBILE MENU =====
        const menuToggle = document.getElementById('menuToggle');
        const navLinks = document.getElementById('navLinks');
        
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });

        // ===== SCROLL REVEAL =====
        const reveals = document.querySelectorAll('.reveal');
        const revealOnScroll = () => {
            reveals.forEach(element => {
                const elementTop = element.getBoundingClientRect().top;
                const windowHeight = window.innerHeight;
                
                if (elementTop < windowHeight - 100) {
                    element.classList.add('active');
                }
            });
        };

        window.addEventListener('scroll', revealOnScroll);
        revealOnScroll();

        // ===== 3D TILT EFFECT FOR CARDS =====
        const cards = document.querySelectorAll('.card-3d');
        
        cards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
            });
        });

        // ===== SMOOTH SCROLL =====
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    </script>

</body>
</html>
"""

# Khai báo tuyến đường gốc nhằm tiếp nhận và phản hồi mọi yêu cầu truy cập từ trình duyệt.
@app.route('/')
def home():
    # Gọi hàm xử lý cấu trúc HTML và gửi về phía máy khách.
    return render_template_string(HTML_TEMPLATE)

# Khởi chạy máy chủ web cục bộ.
if __name__ == '__main__':
    print("=" * 70)
    print("🚀 PORTFOLIO NÂNG CẤP - SIÊU HIỆU ỨNG")
    print("=" * 70)
    print("✨ Typing Effect - Text tự động gõ")
    print("✨ Custom Cursor - Con trỏ chuột tùy chỉnh")
    print("✨ Loading Screen - Màn hình loading chuyên nghiệp")
    print("✨ 3D Tilt Cards - Thẻ nghiêng 3D khi hover")
    print("✨ Animated Gradients - Gradient chuyển động")
    print("✨ Floating Shapes - Các hình dạng bay lượn")
    print("✨ Particles Background - Hạt động nền")
    print("✨ Smooth Animations - Animation mượt mà")
    print("✨ Hover Effects - Hiệu ứng hover đẹp mắt")
    print("✨ Scroll Reveal - Hiển thị khi scroll")
    print("=" * 70)
    print("🌐 Đang chạy tại: http://localhost:5000")
    print("📱 Responsive 100% - Mobile friendly")
    print("🎨 Không cần cài thêm thư viện!")
    print("=" * 70)
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
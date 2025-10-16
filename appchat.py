import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# SETUP API
load_dotenv()
google_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=google_api_key)

# load nội dung menu
menu_df = pd.read_csv('menu.csv', index_col = 0)

# Tạo mô hình
model = genai.GenerativeModel(
    "models/gemini-2.5-flash",
    system_instruction=f"""
        Bạn tên là **PhoBot**, một trợ lý AI có nhiệm vụ hỗ trợ giải đáp thông tin về nhà hàng Việt.
        Các chức năng mà bạn hỗ trợ gồm: {', '.join(menu_df['name'].to_list())}.
        Đối với các câu hỏi ngoài chức năng mà bạn hỗ trợ, trả lời bằng '**Tôi không có thông tin về vấn đề này, tôi chỉ tập trung hỗ trợ thông tin về nhà hàng Viet Cuisine.**'
    """
)

# Hàm trò chuyện '-'
def restaurant_chatbox():
    st.title("Trợ lý nhà hàng Viet Cuisine")
    st.write("Xin chào, tôi là PhoBot, là một chatbox hỗ trợ cung cấp thông tin về nhà hàng Viet Cuisine")
    st.write("Quý khách có thể hỏi tôi về các món ăn và menu của nhà hàng")


    # Nếu chưa có lịch sử
    if 'conver_log' not in st.session_state:
        st.session_state.conver_log = [
            {"role": "assistant", "content": "Xin chào, tôi là PhoBot, tôi có thể giúp gì cho bạn?"}
        ]
    # Nếu đã có lịch sử thì hiển thị sau khi người dùng quay lại
    for message in st.session_state.conver_log:
        if message['role'] != 'system':
            with st.chat_message(message['role']):
                st.write(message['content'])    # Hiển thị tin nhắn('content') theo 'role' 

    # Tạo ô input Prompt
    if prompt := st.chat_input("Hãy nhập câu hỏi của quý khách....."):  # Text hiển thị trong ô input
        # Hiển thị tin nhắn người dùng
        with st.chat_message("user"):
            st.write(prompt)
        # Thêm vào conver_log
        st.session_state.conver_log.append({"role": "user", "content": prompt})

        # Kiểm tra có từ menu và món không
        if "menu" in prompt.lower() or "thực đơn" in prompt.lower():
            bot_reply = '\n\n'.join([f"**{row['name']}** : {row['description']}" for idx, row in menu_df.iterrows()])
        else:
            response = model.generate_content(prompt)
            bot_reply = response.text

        # Hiển thị tin nhắn
        with st.chat_message("assistant"):
            st.write(bot_reply)
        # Thêm vào conver_log
        st.session_state.conver_log.append({"role": "assistant", "content": bot_reply})
                

if __name__ == "__main__":
    restaurant_chatbox()
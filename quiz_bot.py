import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Bật log để theo dõi hoạt động
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Lấy Token từ biến môi trường của Render hoặc dùng token của bạn
TOKEN = os.getenv("BOT_TOKEN", "9079432179:AAEAeCNlpPHVg8fQWgr05B6i_P4JkrNy90c")

# Danh sách 11 câu hỏi điền khuyết Kinh Thánh (Chương 10)
QUIZ_QUESTIONS = [
    {
        "question": "Tôi lại thấy một [1] khác đầy uy lực mặc mây từ trời xuống, trên đầu ngài có [2], gương mặt giống như mặt trời, chân giống như [3]",
        "options": ["sứ giả / hào quang / cột đồng", "thiên sứ / cầu vồng / trụ lửa", "thiên sứ / vương miện / cột lửa"],
        "correct": 1,
        "explanation": "Khải Huyền 10:1 - ...thiên sứ khác đầy uy lực mặc mây từ trời xuống, trên đầu ngài có cầu vồng... chân giống như trụ lửa."
    },
    {
        "question": "Trên tay ngài cầm một [1] nhỏ đã mở, chân phải đạp trên [2], chân trái đạp trên [3]",
        "options": ["tờ giấy / sông / đất", "cuốn sách / biển / sông", "cuốn sách / biển / đất"],
        "correct": 2,
        "explanation": "Khải Huyền 10:2 - Trên tay ngài cầm một cuốn sách nhỏ đã mở, chân phải đạp trên biển, chân trái đạp trên đất."
    },
    {
        "question": "Ngài kêu lớn tiếng như tiếng kêu của [1], khi thiên sứ kêu lên thì bảy [2] cũng kêu lên tiếng",
        "options": ["gấu xám / ngọn lửa", "sư tử / tiếng sấm", "sư tử / ngọn lửa"],
        "correct": 1,
        "explanation": "Khải Huyền 10:3 - Ngài kêu lớn tiếng như tiếng kêu của sư tử, khi thiên sứ kêu lên thì bảy sấm cũng kêu lên tiếng."
    },
    {
        "question": "Khi bảy sấm kêu lên tiếng, tôi định chép lại thì nghe có tiếng từ trời phán “Hãy [1] lại tiếng của bảy sấm đã phán và đừng [2] lại.",
        "options": ["xé rách / đọc", "niêm phong / chép", "giữ / viết"],
        "correct": 1,
        "explanation": "Khải Huyền 10:4 - Hãy niêm phong lại tiếng của bảy sấm đã phán và đừng chép lại."
    },
    {
        "question": "Tôi thấy thiên sứ đạp chân trên [1] và [2] đứng hướng về trời, giơ tay [3] lên,",
        "options": ["mây / núi / trái", "biển / đất / phải", "biển / mây / phải"],
        "correct": 1,
        "explanation": "Khải Huyền 10:5 - Tôi thấy thiên sứ đạp chân trên biển và đất đứng hướng về trời, giơ tay phải lên."
    },
    {
        "question": "Thề và phán với đấng hằng sống đời đời, tức đấng [1] trời và những vật giữa trời, đất và những vật giữa đất, [2] và những vật giữa biển rằng “Sẽ không [3] nữa!”",
        "options": ["cai trị / sông / chờ đợi", "sáng tạo / biển / trì hoãn", "sáng tạo / sông / chậm trễ"],
        "correct": 1,
        "explanation": "Khải Huyền 10:6 - ...tức đấng sáng tạo trời... biển... rằng 'Sẽ không trì hoãn nữa!'"
    },
    {
        "question": "Ngày thiên sứ thứ [1] thổi kèn, khi chiếc kèn ấy được thổi lên, bí mật của Đức Chúa Trời sẽ thành đạt như tin lành đã truyền dạy cho các đầy tớ Ngài là các nhà [2],",
        "options": ["sáu / thầy tế lễ", "bảy / tiên tri", "năm / tiên tri"],
        "correct": 1,
        "explanation": "Khải Huyền 10:7 - Ngày thiên sứ thứ bảy thổi kèn... là các nhà tiên tri."
    },
    {
        "question": "Tôi nghe tiếng từ trời lại phán với tôi rằng “Con hãy đến lấy [1] mở trên tay thiên sứ đang đứng đạp chân trên [2] và [3]”",
        "options": ["tờ giấy / mây / đá", "cuốn sách / biển / đất", "cuốn sách / sông / đất"],
        "correct": 1,
        "explanation": "Khải Huyền 10:8 - ...lấy cuốn sách mở trên tay thiên sứ đang đứng đạp chân trên biển và đất."
    },
    {
        "question": "Tôi tiến đến với thiên sứ và xin ngài cuốn sách, thiên sứ liền bảo tôi “Hãy lấy và [1] đi, ở bụng con sẽ [2] nhưng trên miệng sẽ [3] như mật,”",
        "options": ["giữ / cay / thơm", "ăn / đắng / ngọt", "đọc / đau / ngọt"],
        "correct": 1,
        "explanation": "Khải Huyền 10:9 - ...Hãy lấy và ăn đi, ở bụng con sẽ đắng nhưng trên miệng sẽ ngọt như mật."
    },
    {
        "question": "Tôi lấy và ăn cuốn sách nhỏ từ tay thiên sứ, nó ngọt như [1] trong miệng tôi nhưng sau khi ăn rồi, bụng tôi trở nên [2].",
        "options": ["đường / đau", "mật / đắng", "mật / cồn cào"],
        "correct": 1,
        "explanation": "Khải Huyền 10:10 - ...nó ngọt như mật trong miệng tôi nhưng sau khi ăn rồi, bụng tôi trở nên đắng."
    },
    {
        "question": "Ngài phán với tôi “Con sẽ phải tiên tri lại cho nhiều [1], nhiều nước, nhiều [2] và nhiều [3] nữa.",
        "options": ["người / ngôn ngữ / quan", "dân / thứ tiếng / vua", "đất nước / tiếng nói / người"],
        "correct": 1,
        "explanation": "Khải Huyền 10:11 - ...cho nhiều dân, nhiều nước, nhiều thứ tiếng và nhiều vua nữa."
    }
]

# Lệnh /start: Chào mừng và hướng dẫn
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🎮 Chào mừng bạn đến với **Quiz Kinh Thánh (Khải Huyền Chương 10)**!\n\n"
        "Gõ lệnh `/play` để bắt đầu làm bài trắc nghiệm nhé!"
    )

# Lệnh /play: Tự động phát lần lượt 11 câu hỏi dạng Quiz Poll
async def play_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id, 
        text="🚀 Đang gửi 11 câu hỏi trắc nghiệm điền khuyết. Hãy chọn đáp án chính xác nhất cho từng câu dưới đây:"
    )

    for i, q in enumerate(QUIZ_QUESTIONS, 1):
        question_text = f"Câu {i}: {q['question']}"
        await context.bot.send_poll(
            chat_id=chat_id,
            question=question_text,
            options=q["options"],
            type="quiz",
            correct_option_id=q["correct"],
            explanation=q["explanation"],
            is_anonymous=False,
        )

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play_quiz))

    print("Bot Quiz đang chạy ở chế độ Polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
import asyncio
import os

# Import the main financial service agent
from customer_service_agent.agent import financial_service_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history_async, call_agent_async

load_dotenv()

# Debug: Check if API key is loaded
print(
    f"GOOGLE_API_KEY loaded: {'Yes' if os.getenv('GOOGLE_API_KEY') else 'No'}")
if os.getenv('GOOGLE_API_KEY'):
    print(f"API Key starts with: {os.getenv('GOOGLE_API_KEY')[:10]}...")

# ===== PART 1: Initialize In-Memory Session Service =====
# Using in-memory storage for this example (non-persistent)
session_service = InMemorySessionService()


# ===== PART 2: Define Initial State =====
# This will be used when creating a new session
initial_state = {
    "user_name": "Nguyễn Văn A",
    "financial_profile": {
        "student_id": "SV001",
        "university": "Đại học Kinh tế TP.HCM",
        "year": 3,
        "major": "Tài chính ngân hàng",
        "monthly_income": 5000000,  # từ part-time job
        "current_savings": 15000000,
        "financial_goals": ["du học", "mua laptop", "tiết kiệm dài hạn"]
    },
    "interaction_history": [],
}


async def main_async():
    # Setup constants
    APP_NAME = "SACOMBANK Financial Service"
    USER_ID = "student_user"

    # ===== PART 3: Session Creation =====
    # Create a new session with initial state
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id
    print(f"Tạo phiên làm việc mới: {SESSION_ID}")

    # ===== PART 4: Agent Runner Setup =====
    # Create a runner with the main financial service agent
    runner = Runner(
        agent=financial_service_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== PART 5: Interactive Conversation Loop =====
    print("\nChào mừng đến với Dịch vụ Tư vấn Tài chính SACOMBANK!")
    print("Nhập 'exit' hoặc 'quit' để kết thúc cuộc trò chuyện.\n")

    while True:
        # Get user input
        user_input = input("Bạn: ")

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit", "thoát", "kết thúc"]:
            print("Kết thúc cuộc trò chuyện. Cảm ơn bạn đã sử dụng dịch vụ SACOMBANK!")
            break

        # Update interaction history with the user's query
        await add_user_query_to_history_async(
            session_service, APP_NAME, USER_ID, SESSION_ID, user_input
        )

        # Process the user query through the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    # ===== PART 6: State Examination =====
    # Show final session state
    final_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print("\nTrạng thái phiên làm việc cuối cùng:")
    for key, value in final_session.state.items():
        print(f"{key}: {value}")


def main():
    """Entry point for the application."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

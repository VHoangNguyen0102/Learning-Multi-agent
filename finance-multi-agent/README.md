# Hệ thống Multi-Agent Tài chính SACOMBANK

Dự án này minh họa cách tạo ra một hệ thống multi-agent có trạng thái trong ADK, kết hợp sức mạnh của quản lý trạng thái liên tục với việc phân công nhiệm vụ cho các agent chuyên biệt. Phương pháp này tạo ra hệ thống agent thông minh có thể ghi nhớ thông tin người dùng qua các tương tác và tận dụng chuyên môn của từng lĩnh vực.

## Hệ thống Multi-Agent Tài chính là gì?

Hệ thống Multi-Agent Tài chính kết hợp hai mô hình mạnh mẽ:

1. **Quản lý Trạng thái**: Lưu trữ thông tin về người dùng và cuộc trò chuyện qua các tương tác
2. **Kiến trúc Multi-Agent**: Phân phối nhiệm vụ giữa các agent chuyên biệt dựa trên chuyên môn của họ

Kết quả là một hệ sinh thái agent tinh vi có thể:

- Ghi nhớ thông tin người dùng và lịch sử tương tác
- Định tuyến truy vấn đến agent chuyên biệt phù hợp nhất
- Cung cấp phản hồi cá nhân hóa dựa trên các tương tác trước đó
- Duy trì ngữ cảnh qua nhiều lần ủy quyền agent

Ví dụ này triển khai hệ thống tư vấn tài chính cho sinh viên của SACOMBANK, nơi các agent chuyên biệt xử lý các khía cạnh khác nhau của dịch vụ tài chính trong khi chia sẻ trạng thái chung.

## Cấu trúc Dự án

```
finance-multi-agent/
│
├── customer_service_agent/         # Gói agent chính
│   ├── __init__.py                 # Bắt buộc cho ADK discovery
│   ├── agent.py                    # Định nghĩa agent gốc
│   └── sub_agents/                 # Các agent chuyên biệt
│       ├── loan_agent/             # Xử lý khoản vay học tập & du học
│       ├── saving_agent/           # Quản lý tiết kiệm sinh viên
│       ├── finance_offer_agent/    # Ưu đãi tài chính sinh viên
│       └── budget_and_planning_agent/ # Hỗ trợ quản lý tài chính cá nhân
│
├── main.py                         # Điểm vào ứng dụng với thiết lập phiên
├── utils.py                        # Hàm hỗ trợ quản lý trạng thái
├── .env                            # Biến môi trường
└── README.md                       # Tài liệu này
```

## Các Thành phần Chính

### 1. Quản lý Phiên

Ví dụ sử dụng `InMemorySessionService` để lưu trữ trạng thái phiên:

```python
session_service = InMemorySessionService()

def initialize_state():
    """Khởi tạo trạng thái phiên với các giá trị mặc định."""
    return {
        "user_name": "Nguyễn Văn A",
        "financial_profile": {
            "student_id": "SV001",
            "university": "Đại học Kinh tế TP.HCM",
            "year": 3,
            "major": "Tài chính ngân hàng",
            "monthly_income": 5000000,
            "current_savings": 15000000,
            "financial_goals": ["du học", "mua laptop", "tiết kiệm dài hạn"]
        },
        "interaction_history": [],
    }

# Tạo phiên mới với trạng thái ban đầu
session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initialize_state(),
)
```

### 2. Chia sẻ Trạng thái giữa các Agent

Tất cả agent trong hệ thống có thể truy cập cùng một trạng thái phiên, cho phép:

- Agent gốc theo dõi lịch sử tương tác
- Loan agent cập nhật thông tin vay
- Saving agent kiểm tra khả năng tài chính của sinh viên
- Tất cả agent cá nhân hóa phản hồi dựa trên thông tin người dùng

### 3. Phân công Multi-Agent

Agent dịch vụ tài chính định tuyến truy vấn đến các sub-agent chuyên biệt:

```python
financial_service_agent = Agent(
    name="financial_service",
    model="gemini-2.0-flash",
    description="Tư vấn viên tài chính SACOMBANK cho sinh viên",
    instruction="""
    Bạn là tư vấn viên tài chính chính của SACOMBANK, chuyên phục vụ sinh viên.
    Vai trò của bạn là hỗ trợ sinh viên với các câu hỏi về tài chính và chuyển họ đến agent chuyên biệt phù hợp.

    # ... hướng dẫn chi tiết ...

    """,
    sub_agents=[loan_agent, saving_agent, finance_offer_agent, budget_and_planning_agent],
    tools=[],
)
```

## Cách thức Hoạt động

1. **Tạo Phiên Ban đầu**:

   - Phiên mới được tạo với thông tin sinh viên và lịch sử tương tác trống
   - Trạng thái phiên được khởi tạo với các giá trị mặc định

2. **Theo dõi Cuộc trò chuyện**:

   - Mỗi tin nhắn của người dùng được thêm vào `interaction_history` trong trạng thái
   - Các agent có thể xem lại các tương tác trước để duy trì ngữ cảnh

3. **Định tuyến Truy vấn**:

   - Agent gốc phân tích truy vấn của người dùng và quyết định chuyên gia nào nên xử lý
   - Các agent chuyên biệt nhận toàn bộ ngữ cảnh trạng thái khi được ủy quyền

4. **Cập nhật Trạng thái**:

   - Khi sinh viên thực hiện giao dịch tài chính, các agent cập nhật thông tin hồ sơ
   - Những cập nhật này có sẵn cho tất cả agent cho các tương tác tương lai

5. **Phản hồi Cá nhân hóa**:
   - Các agent điều chỉnh phản hồi dựa trên hồ sơ tài chính và tương tác trước đó
   - Các đường dẫn khác nhau được thực hiện dựa trên những gì sinh viên đã từng quan tâm

## Các Agent Chuyên biệt

### 1. Loan Agent (Chuyên viên Khoản vay)

- **Chức năng**: Tư vấn khoản vay học tập và du học
- **Dịch vụ chính**:
  - Hướng dẫn thủ tục vay học tập (hồ sơ, giấy tờ, điều kiện)
  - Tư vấn khoản vay du học (ngoại tệ, thời hạn, lãi suất)
  - Ước tính hạn mức vay dựa trên thông tin sinh viên
  - Theo dõi tiến độ xử lý hồ sơ vay

### 2. Saving Agent (Chuyên viên Tiết kiệm)

- **Chức năng**: Tư vấn tiết kiệm sinh viên
- **Dịch vụ chính**:
  - Giới thiệu các gói tiết kiệm cho sinh viên
  - So sánh lãi suất tiết kiệm ngắn hạn và dài hạn
  - Tư vấn cách lập kế hoạch tiết kiệm để đạt mục tiêu
  - Hỗ trợ tiết kiệm cho học phí, du học, mua laptop

### 3. Finance Offer Agent (Chuyên viên Ưu đãi Tài chính)

- **Chức năng**: Tư vấn ưu đãi tài chính sinh viên
- **Dịch vụ chính**:
  - Tìm kiếm và liệt kê các ưu đãi hiện hành
  - Gợi ý lựa chọn sản phẩm tài chính phù hợp nhu cầu
  - Thông tin về thẻ tín dụng sinh viên, miễn phí dịch vụ
  - Chương trình khuyến mãi đặc biệt

### 4. Budget & Planning Agent (Chuyên viên Quản lý Tài chính)

- **Chức năng**: Hỗ trợ quản lý tài chính cá nhân
- **Dịch vụ chính**:
  - Hướng dẫn lập ngân sách cá nhân
  - Theo dõi thu chi hàng tháng
  - Đưa ra cảnh báo khi vượt chi tiêu dự kiến
  - Lập kế hoạch tài chính dài hạn

## Bắt đầu

### Thiết lập

1. Kích hoạt môi trường ảo từ thư mục gốc:

```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. Đảm bảo Google API key được đặt trong file `.env`:

```
GOOGLE_API_KEY=your_api_key_here
```

### Chạy Ví dụ

Để chạy ví dụ multi-agent tài chính:

```bash
python main.py
```

This will:

1. Initialize a new session with default state
2. Start an interactive conversation with the customer service agent
3. Track all interactions in the session state
4. Allow specialized agents to handle specific queries

### Example Conversation Flow

Try this conversation flow to test the system:

1. **Start with a general query**:

   - "What courses do you offer?"
   - (Root agent will route to sales agent)

2. **Ask about purchasing**:

   - "I want to buy the AI Marketing Platform course"
   - (Sales agent will process the purchase and update state)

3. **Ask about course content**:

   - "Can you tell me about the content in the AI Marketing Platform course?"
   - (Root agent will route to course support agent, which now has access)

4. **Ask about refunds**:
   - "What's your refund policy?"
   - (Root agent will route to policy agent)

Notice how the system remembers your purchase across different specialized agents!

## Advanced Features

### 1. Interaction History Tracking

The system maintains a history of interactions to provide context:

```python
# Update interaction history with the user's query
add_user_query_to_history(
    session_service, APP_NAME, USER_ID, SESSION_ID, user_input
)
```

### 2. Dynamic Access Control

The system implements conditional access to certain agents:

```
3. Course Support Agent
   - For questions about course content
   - Only available for courses the user has purchased
   - Check if "ai_marketing_platform" is in the purchased courses before directing here
```

### 3. State-Based Personalization

All agents tailor responses based on session state:

```
Tailor your responses based on the user's purchase history and previous interactions.
When the user hasn't purchased any courses yet, encourage them to explore the AI Marketing Platform.
When the user has purchased courses, offer support for those specific courses.
```

## Production Considerations

For a production implementation, consider:

1. **Persistent Storage**: Replace `InMemorySessionService` with `DatabaseSessionService` to persist state across application restarts
2. **User Authentication**: Implement proper user authentication to securely identify users
3. **Error Handling**: Add robust error handling for agent failures and state corruption
4. **Monitoring**: Implement logging and monitoring to track system performance

## Additional Resources

- [ADK Sessions Documentation](https://google.github.io/adk-docs/sessions/session/)
- [ADK Multi-Agent Systems Documentation](https://google.github.io/adk-docs/agents/multi-agent-systems/)
- [State Management in ADK](https://google.github.io/adk-docs/sessions/state/)

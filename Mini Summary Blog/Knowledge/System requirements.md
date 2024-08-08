# Các yêu cầu cơ bản khi thiết kế hệ thống (Basic requirements when designing the system):
     Tóm tắt:
        I. Yêu cầu chung khi thiết kế hệ thống (General requirements):
            1. Scalability
            2. Modularity
            3. Flexibility
            4. Maintainability
            5. Security
            6. Reliability
            7. Performance
            8. Testability
            9. Cost-effectiveness
            10. Usability
        II. Yêu cầu phi tính năng (Functional Requirements):
            1. Các trường hợp sử dụng của chức năng (Use Case Functions):
                - Tên trường hợp sử dụng của chức năng (Use Case Name)
                - Tóm tắt (Summary)
                - Luồng chạy cơ bản (Basic Flow) 
                - Luồng thay thế (Alternative flow)
                - Điểm mở rộng (Extension point)
                - Điều kiện trước tiên (Preconditions)
                - Điều kiện sau cùng (Postconditions)
                - Logic nghiệp vụ (Business Logic)
            2. Thiết kế luồng hoạt động (Flow Design):
                - Link web thiết kế flow: draw.io / miro.com
                a. Thiết kế cấp cao (HLD: High-Level Design)
                b. Thiết kế cấp thấp (LLD: Low-Level Design)
                c. Sử dụng uml
        III. Yêu cầu phi tính năng (Non-Functional Requirements)
            - Số lượng, lưu lượng của user cùng lúc
            - Thời gian phản hồi
            - Thời gian hoạt động của hệ thống (uptime)
            - Mã hóa
            - Bảo mật
            
## I. Yêu cầu chung khi thiết kế hệ thống (General requirements)
- Scalability: Hệ thống phải có khả năng xử lý số lượng người dùng và yêu cầu ngày càng tăng mà không làm giảm hiệu suất đáng kể.
- Modularity: Hệ thống nên được chia thành các Module nhỏ, độc lập, có thể dễ dàng thay thế hoặc cập nhật.
- Flexibility: Hệ thống phải có khả năng thích ứng với các yêu cầu thay đổi và các tính năng mới.
- Maintainability: Hệ thống phải dễ hiểu, dễ khắc phục sự cố.
- Security: Hệ thống phải được thiết kế để bảo vệ chống lại các cuộc tấn công độc hại và truy cập trái phép.
- Reliability: Hệ thống phải được thiết kế để giảm thiểu thời gian ngừng hoạt động và mất mác dữ liệu.
- Performance: Hệ thống phải được thiết kế để đáp ứng các yêu cầu về hiệu suất, chẳng hạn như thời gian phản hồi nhanh.
- Testability: Hệ thống phải được thiết kế để tạo điều kiện thuận lợi cho việc kiểm tra, debug và giám sát.
- Cost-effectiveness: Hệ thống cần được thiết kế để giảm thiểu chi phí phát triển và bảo trì.
- Usability: Hệ thống phải được thiết kế thân thiện và dễ sử dụng.
## II. Yêu cầu tính năng (Functional Requirements)
### 1. Các trường hợp sử dụng của chức năng (Use Case Functions):
- Tên trường hợp sử dụng của chức năng (Use Case Name)
- Tóm tắt (Summary)
- Luồng chạy cơ bản (Basic Flow) 
- Luồng thay thế (Alternative flow)
- Điểm mở rộng (Extension point)
- Điều kiện trước tiên (Preconditions)
- Điều kiện sau cùng (Postconditions)
- Logic nghiệp vụ (Business Logic)
### 2. Thiết kế luồng hoạt động (Flow Design):
- a. Thiết kế cấp cao (HLD: High-Level Design)
    - Architecture Diagram: Các thành phần chính như máy chủ web, máy chủ ứng dụng, cơ sở dữ liệu, các dịch vụ bên ngoài, và cách chúng tương tác với nhau.
    - Data Flow Diagram: Các luồng dữ liệu giữa các thành phần chính, điểm đầu vào và đầu ra của dữ liệu.
    - Component Diagram: Các phần mềm như mô-đun, thư viện, và các dịch vụ, cùng với các giao diện và kết nối giữa chúng.
    - Deployment Diagram: Minh họa cách phần mềm được triển khai trên phần cứng.
    - Use Case Diagram: Minh họa các trường hợp sử dụng của hệ thống và mối quan hệ giữa các tác nhân (actors) và các trường hợp sử dụng (use cases).
- b. Thiết kế cấp thấp (LLD: Low-Level Design)
    - Class Diagram: Các class, thuộc tính của chúng, các phương thức và mối quan hệ (kế thừa, liên kết, phụ thuộc) giữa các class.
    - Sequence Diagram: Các đối tượng tham gia, thứ tự các tin nhắn trao đổi giữa chúng, và thời gian diễn ra các hoạt động.
    - Activity Diagram: Mô tả luồng công việc hoặc hoạt động trong một quy trình nghiệp vụ hoặc một phần của hệ thống
    - State Diagram: Các trạng thái của đối tượng, các sự kiện kích hoạt chuyển đổi trạng thái và các hành động liên quan.
    - Entity-Relationship Diagram: Cấu trúc dữ liệu và mối quan hệ giữa các thực thể dữ liệu.
- c. Sử dụng uml (Unified Modeling Language - Ngôn ngữ mô hình thống nhất) để thiết kế bảng
    - [UML](https://200lab.io/blog/uml-la-gi-gioi-thieu-cac-loai-uml-hay-dung/)
### III. Yêu cầu phi tính năng (Non-Functional Requirements)
- Số lượng, lưu lượng của user cùng lúc
- Thời gian phản hồi
- Thời gian hoạt động của hệ thống (uptime)
- Mã hóa
- Bảo mật

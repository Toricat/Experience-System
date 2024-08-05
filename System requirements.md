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
            2. Thiết kế luồng hoạt động:
            [Link bài viết: Kiến trúc phân lớp](https://200lab.io/blog/cach-phan-loai-cac-loai-kien-truc-phan-mem-phan-1/)
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
### 2.
### III. Yêu cầu phi tính năng (Non-Functional Requirements)
- Số lượng, lưu lượng của user cùng lúc
- Thời gian phản hồi
- Thời gian hoạt động của hệ thống (uptime)
- Mã hóa
- Bảo mật

# Requirements — StudyFlow

## 1. Functional Requirements

Câu chữ dưới đây là baseline đề xuất đã điều chỉnh theo mô hình Fixed Recurrence Batch. Các trường/Use Case đánh dấu Phase 2 chỉ có hiệu lực khi Phase 2 được triển khai.

### FR01 — Xem kế hoạch tuần
Hệ thống cho phép người dùng xem các Activity Instance được lên lịch trong một tuần, kèm Schedule của từng instance.

**Source:** UN01

### FR02 — Xem hoạt động theo ngày
Hệ thống cho phép người dùng xem các Activity Instance được lên lịch trong một ngày cụ thể theo thứ tự thời gian.

**Source:** UN01

### FR03 — Tạo Activity và Activity Instance
Hệ thống cho phép người dùng tạo Activity và các Activity Instance tương ứng. Nếu không lặp, hệ thống tạo một instance với Schedule hợp lệ; nếu lặp, hệ thống tạo toàn bộ Fixed Recurrence Batch trong khoảng thời gian được chọn.

**Source:** UN02, UN03

### FR04 — Chỉnh sửa định nghĩa Activity
Nếu chức năng chỉnh sửa Activity cha được cung cấp, hệ thống cho phép chỉnh sửa định nghĩa/metadata của Activity nhưng không tự động thay đổi dữ liệu của Activity Instance đã tồn tại. Việc chỉnh sửa Recurrence sau khi batch được tạo không được hỗ trợ trong MVP.

**Source:** UN02, UN03

### FR04.1 — Chỉnh sửa Activity Instance
Hệ thống cho phép người dùng chỉnh sửa dữ liệu thực tế của một Activity Instance. Với instance thuộc Fixed Recurrence Batch, người dùng có thể chọn chỉ áp dụng cho instance được chọn hoặc áp dụng các thuộc tính đã thay đổi cho instance được chọn và các instance tương lai đủ điều kiện.

**Source:** UN02, UN03

### FR05 — Thiết lập Schedule
Hệ thống cho phép người dùng đặt `schedule_date`, `start_time` và `end_time` trực tiếp trên Activity Instance. Đây là ba thuộc tính cấu thành Schedule; không có bảng Schedule riêng. Cả ba trường đều bắt buộc và giờ kết thúc phải sau giờ bắt đầu.

**Source:** UN03

### FR06 — Thiết lập Priority
Hệ thống cho phép đặt Priority mặc định trong quá trình tạo Activity và lưu Priority thực tế riêng ở từng Activity Instance. Giá trị hợp lệ là `LOW`, `MEDIUM`, `HIGH`.

**Source:** UN02

### FR06.1 — Sắp xếp Activity Instance theo Priority
Hệ thống cho phép người dùng xem các Activity Instance sắp diễn ra được sắp xếp theo Priority theo thứ tự HIGH → MEDIUM → LOW; các instance cùng Priority được sắp xếp theo thời điểm bắt đầu Schedule tăng dần.

**Source:** UN01, UN02

### FR07 — Thiết lập Deadline
Hệ thống cho phép đặt, thay đổi hoặc xóa Deadline của một Activity Instance. Deadline là tùy chọn và thuộc từng instance.

**Source:** UN03, UN05

### FR08 — Thiết lập Reminder
Hệ thống cho phép thiết lập nhiều Reminder cho một Activity Instance dựa trên Schedule hoặc Deadline của chính instance. Không cho phép hai Reminder cùng instance có cùng `trigger_type` và `offset_minutes`, kể cả khi cấu hình đang disabled. Khi tạo batch lặp, Reminder theo Schedule được tạo riêng cho từng instance với cùng offset; Reminder theo Deadline chỉ hợp lệ khi instance có Deadline. Nếu thời điểm kích hoạt đã qua, hệ thống bỏ qua, không gửi bù.

**Source:** UN05

### FR08.1 — Thông báo Reminder
Trong MVP, khi trang StudyFlow đang mở và JavaScript đang chạy, frontend định kỳ kiểm tra các Reminder đến hạn và hiển thị thông báo trong giao diện. MVP không yêu cầu thông báo khi trang StudyFlow đã đóng và không triển khai browser push notification.

**Source:** UN05

### FR09 — Thiết lập Recurrence khi tạo
Hệ thống cho phép người dùng cấu hình Recurrence DAILY (mỗi N ngày) hoặc WEEKLY (một/nhiều ngày trong tuần, mỗi N tuần) khi tạo Activity. Khoảng batch tính cả ngày bắt đầu/kết thúc và không vượt quá một năm. Với WEEKLY, ngày bắt đầu phải nằm trong tập ngày đã chọn. Recurrence không thể chỉnh sửa để tái cấu trúc batch sau khi tạo.

**Source:** UN03

### FR09.1 — Tạo Fixed Recurrence Batch
Khi Activity có Recurrence, hệ thống tạo toàn bộ Activity Instance tương ứng với các lần diễn ra trong khoảng thời gian đã chọn. Batch tối đa một năm; Deadline của mỗi instance mặc định là NULL. Sau khi tạo thành công, hệ thống không tự động sinh thêm instance và không đồng bộ lại tập instance do thay đổi Recurrence.

**Source:** UN03

### FR10 — Thiết lập Location (Phase 2)
Hệ thống cho phép thiết lập Location mặc định cho Activity và Location riêng cho Activity Instance khi chức năng được triển khai.

**Source:** UN02, UN03

### FR11 — Gắn Tag (Phase 2)
Hệ thống cho phép gắn một hoặc nhiều Tag cho Activity khi chức năng được triển khai. Tag không được ghi đè riêng trên Activity Instance; có thể lọc instance thông qua Tag của Activity cha.

**Source:** UN02

### FR12 — Lọc theo Tag (Phase 2)
Hệ thống cho phép lọc Activity theo Tag và hiển thị các Activity Instance thuộc những Activity phù hợp.

**Source:** UN02

### FR13 — Gán Subject (Phase 2)
Hệ thống cho phép gán Subject mặc định cho Activity và tùy chỉnh Subject riêng cho Activity Instance khi chức năng được triển khai.

**Source:** UN02

### FR14 — Cập nhật Status của Activity Instance
Hệ thống cho phép người dùng cập nhật Status của một Activity Instance thành NOT_STARTED, IN_PROGRESS hoặc COMPLETED mà không thay đổi Status của các instance khác. Hệ thống không tự chuyển Status chỉ vì Schedule đã qua.

**Source:** UN04

### FR15 — Xem trạng thái và tiến độ
Hệ thống cho phép người dùng xem trạng thái và mức độ hoàn thành của các Activity Instance trong một khoảng thời gian, bao gồm số lượng instance đã hoàn thành.

**Source:** UN04

### FR16 — Xem Activity Instance sắp diễn ra
Khi các Activity Instance được lên lịch trong ngày hiện tại đã kết thúc theo Schedule, hệ thống cho phép người dùng xem các Activity Instance sắp diễn ra.

**Source:** UN01

### FR16.1 — Sắp xếp/lọc hoạt động sắp diễn ra
Hệ thống cho phép người dùng thay đổi cách sắp xếp hoặc áp dụng bộ lọc được hỗ trợ cho các Activity Instance sắp diễn ra, bao gồm Schedule và Priority.

**Source:** UN01, UN02

### FR17 — Xóa Activity
Hệ thống cho phép người dùng xóa một Activity sau khi xác nhận. Khi xóa thành công, hệ thống xóa cấu hình Recurrence, toàn bộ Activity Instance và Reminder phụ thuộc. Việc xóa riêng một Activity Instance được quy định tại FR18.

**Source:** UN06

### FR18 — Xóa Activity Instance
Hệ thống cho phép người dùng xóa một Activity Instance sau khi xác nhận nếu Activity cha vẫn còn ít nhất một instance khác. Khi xóa, các Reminder của instance đó bị xóa theo; các instance còn lại giữ nguyên `series_position` và hệ thống không tạo occurrence bù. Nếu đây là instance cuối cùng, hệ thống không cho xóa riêng mà hướng người dùng xóa Activity cha.

**Source:** UN02, UN06

---

## 2. Non-functional Requirements

### NFR01 — Reliability
Sau khi thao tác lưu thành công, dữ liệu phải vẫn chính xác sau khi tải lại hoặc mở lại ứng dụng.

**Initial target:** dữ liệu của thao tác đã xác nhận thành công không bị mất hoặc tự thay đổi trong những lần sử dụng tiếp theo.

### NFR02 — Data Integrity
Hệ thống phải duy trì tính nhất quán giữa Activity, Activity Instance, Schedule, Deadline, Reminder, Status và các dữ liệu Phase 2. Chỉnh sửa một instance không được tự động thay đổi các instance khác. Chỉnh sửa Activity cha không được tự động cập nhật instance đã tồn tại.

### NFR03 — Responsiveness
Giao diện phản ánh thay đổi sau khi thao tác được xử lý thành công.

**Initial target:** với thao tác thông thường trong điều kiện sử dụng dự kiến, giao diện phản ánh kết quả trong vòng 1 giây sau khi hệ thống xác nhận thành công.

### NFR04 — Reminder Timeliness
Hệ thống thông báo gần thời điểm Reminder đến hạn.

**Initial target:** hiển thị thông báo trong vòng 1 phút kể từ lúc Reminder đến hạn khi trang StudyFlow vẫn mở, trình duyệt hoạt động và frontend tiếp tục chạy. Không bảo đảm khi tab bị treo, trình duyệt đóng hoặc thiết bị ngủ. Nếu thời điểm kích hoạt đã qua trước khi trang kiểm tra được Reminder, hệ thống bỏ qua và không gửi bù.

### NFR05 — Usability
Giao diện trực quan, nhất quán và dễ hiểu; kế hoạch ngày hiện tại nhìn thấy trực tiếp từ màn hình chính; Name, Schedule, Priority và Status được trình bày nhất quán; thao tác thường dùng dễ truy cập.

### NFR06 — Privacy and Security
MVP trước mắt chỉ được sử dụng riêng tư. Không công khai ứng dụng khi chưa có biện pháp kiểm soát truy cập phù hợp. Trước khi public deployment, phải bổ sung và kiểm thử authentication, authorization, secure configuration và bảo vệ dữ liệu; multi-user và data isolation theo từng tài khoản thuộc phạm vi tương lai.

---

## 3. Business Rules

### BR01 — Subject Association (Phase 2)
Activity có thể có Subject mặc định hoặc không có Subject. Khi Phase 2 được triển khai, Subject có thể được tùy chỉnh riêng cho một Activity Instance.

### BR02 — Activity Instance Scheduling
Mỗi Activity Instance được tạo thành công phải có đủ ba thuộc tính Schedule hợp lệ, lưu trực tiếp trên instance; không có entity/bảng Schedule. Activity không lặp tạo một instance với `series_position = 1`; Activity lặp tạo batch hữu hạn.

### BR03 — Activity–Instance Relationship
Mỗi Activity Instance thuộc đúng một Activity cha. Instance là weak entity, định danh bằng khóa ghép `(activity_id, series_position)`; `series_position` là partial key bất biến. Instance vẫn thuộc Activity cha dù Schedule hoặc thuộc tính khác được chỉnh sửa riêng. Xóa Activity sẽ cascade xóa các instance và Reminder phụ thuộc.

### BR04 — Instance Status
Status được quản lý riêng cho từng Activity Instance, chỉ nhận `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`; cập nhật Status không làm thay đổi instance khác. Status không tự động đổi khi Schedule đã qua.

### BR05 — Optional Deadline per Instance
Mỗi Activity Instance có thể có Deadline hoặc không. Deadline được lưu cho từng instance, không bắt buộc dùng chung một thời điểm tuyệt đối cho tất cả instance của batch.

### BR06 — Reminder per Instance
Reminder thuộc một Activity Instance và dựa trên Schedule hoặc Deadline của chính instance. Reminder theo Deadline chỉ hợp lệ khi instance có Deadline; nếu Deadline bị xóa thì Reminder theo Deadline bị xóa theo. Cấu hình trùng `(instance, trigger_type, offset_minutes)` không được phép, dù Reminder bị disabled. Reminder disabled hoặc đã quá thời điểm kích hoạt không được gửi.

### BR07 — Daily Activity Ordering
Các Activity Instance trong chế độ xem ngày được sắp xếp theo thời điểm bắt đầu Schedule.

### BR08 — Upcoming Activity Display
Trên màn hình chính, hệ thống hiển thị kế hoạch ngày hiện tại theo trình tự thời gian. Khi tất cả Schedule của những hoạt động trong ngày đã kết thúc, hệ thống chuyển trọng tâm sang các Activity Instance sắp diễn ra trong tương lai.

### BR09 — Upcoming Activity Ordering
Các Activity Instance sắp diễn ra mặc định được sắp xếp theo Priority; các instance cùng Priority được sắp xếp theo Schedule. Người dùng có thể thay đổi tiêu chí sắp xếp hoặc dùng bộ lọc được hỗ trợ.

### BR10 — Recurrence Limit and Fixed Batch
Recurrence chỉ hỗ trợ DAILY và WEEKLY, sinh toàn bộ Activity Instance trong một khoảng thời gian bao gồm hai đầu mút, tối đa một năm tính từ ngày bắt đầu. DAILY là mỗi N ngày; WEEKLY là các ngày đã chọn mỗi N tuần và phải bao gồm weekday của ngày bắt đầu. Toàn bộ batch được tạo khi Activity được lưu thành công.

### BR11 — Activity Instance Data Independence
Mỗi Activity Instance lưu dữ liệu thực tế riêng, bao gồm Status, Name, Description, Priority, ba thuộc tính Schedule, Deadline, Reminder và các thuộc tính Phase 2 khi được triển khai. Thay đổi ở một instance không tự động thay đổi instance khác.

### BR12 — Activity Name Optional
Activity có thể được tạo mà không cần Name. Quy tắc này không miễn trừ yêu cầu Schedule cho từng instance.

### BR13 — Edit Instance Scope
Khi chỉnh sửa instance thuộc Fixed Recurrence Batch, hệ thống cho phép chọn chỉ áp dụng cho instance được chọn hoặc áp dụng các thuộc tính đã thay đổi cho instance được chọn và các instance tương lai đủ điều kiện. Lựa chọn bulk chỉ được cung cấp khi instance được chọn có Schedule ở tương lai và Status chưa Completed; nếu instance được chọn đã ở quá khứ hoặc đã Completed, người dùng chỉ có thể chỉnh sửa riêng instance đó.

### BR14 — Single-Instance Edit
Khi chỉ áp dụng cho instance được chọn, chỉ dữ liệu của instance đó được cập nhật. Instance tiếp tục thuộc Activity cha và giữ nguồn gốc của batch. Chỉnh sửa thuộc tính không liên quan đến Schedule không tự tạo Schedule exception.

### BR15 — Editing Activity Definition
Chỉnh sửa Activity cha không tự động thay đổi Activity Instance đã tồn tại. Giá trị định nghĩa/default được dùng để khởi tạo dữ liệu ở thời điểm tạo batch; sau đó dữ liệu instance được quản lý riêng.

### BR16 — Explicit Bulk Update
Thay đổi hàng loạt chỉ thực hiện khi người dùng chủ động chọn phạm vi áp dụng. Chỉ những thuộc tính nằm trong nội dung thay đổi mới được cập nhật; các thuộc tính khác không bị ghi đè.

### BR17 — Schedule Exception
Nếu người dùng đổi riêng một trong các thuộc tính Schedule (`schedule_date`, `start_time`, `end_time`), đặt `schedule_exception = true`. Thao tác bulk Schedule chỉ đổi giờ bắt đầu/kết thúc, giữ ngày và không ghi đè Schedule ngoại lệ. Thay đổi Name, Description, Priority, Deadline hoặc Reminder không tự tạo Schedule exception.

### BR18 — Recurrence Configuration Is Fixed After Creation
Sau khi Fixed Recurrence Batch được tạo, không cho sửa Recurrence để tạo thêm, loại bỏ hoặc tái lập lịch hàng loạt các occurrence. Muốn tạo giai đoạn tiếp theo hoặc dùng quy tắc lặp khác, người dùng tạo Activity mới.

### BR19 — Protect Past and Completed Instances
Cập nhật hàng loạt không được thay đổi những instance có thời điểm Schedule đã qua hoặc có Status là Completed. Người dùng vẫn có thể chỉnh sửa riêng một instance quá khứ nếu hệ thống cho phép thao tác đó.

### BR20 — Initialize Instance Values
Khi tạo batch, ngày của từng instance được sinh theo Recurrence; thời gian bắt đầu/kết thúc được khởi tạo từ form và sao chép vào các thuộc tính `start_time`/`end_time` của từng instance. Các thuộc tính mặc định khác của Activity được sao chép vào instance khi tạo. Sau khi được tạo, các giá trị thực tế của instance được lưu riêng; chỉnh sửa Activity cha sau đó không làm cập nhật lại instance.

### BR21 — Schedule Conflict
Nếu khoảng thời gian Schedule mới chồng lấn Schedule của một Activity Instance khác trong cùng ngày, hệ thống cảnh báo nhưng cho phép người dùng xác nhận bỏ qua. Dùng khoảng nửa mở `[start, end)`: `start_A < end_B AND start_B < end_A`; hai lịch nối tiếp tại mốc kết thúc không chồng lấn.

### BR22 — Tag Association (Phase 2)
Khi Tag được triển khai, Tag chỉ gắn với Activity. Lọc Activity Instance theo Tag thông qua Activity cha; không có liên kết Tag riêng cho instance trong thiết kế Phase 2 đã chốt.

### BR23 — Bulk Update Eligibility
Một instance đủ điều kiện cập nhật hàng loạt khi Schedule của nó vẫn ở tương lai và Status chưa Completed. Instance quá khứ dù chưa hoàn thành vẫn bị bảo vệ khỏi cập nhật hàng loạt. Schedule exception chỉ bảo vệ Schedule; các thuộc tính khác có thể cập nhật nếu nằm trong phạm vi người dùng đã chọn.

### BR24 — No Automatic Recurrence Regeneration
Hệ thống không tự tạo occurrence bù hoặc tự đồng bộ batch khi người dùng sửa một thuộc tính instance. Việc chỉnh sửa instance không làm thay đổi số lượng instance đã tạo.

### BR25 — Fixed Status and Priority Values
Status chỉ nhận `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`; Priority chỉ nhận `LOW`, `MEDIUM`, `HIGH`. Status không tự đổi chỉ vì Schedule đã qua.

### BR26 — Activity Instance Identification and Cascade Delete
Activity Instance là weak entity có khóa ghép `(activity_id, series_position)`; `series_position` bất biến. Xóa Activity sẽ xóa Recurrence, toàn bộ Activity Instance và Reminder phụ thuộc theo cascade. Có thể xóa riêng một instance nếu Activity vẫn còn ít nhất một instance; Reminder của instance đó cascade và các vị trí còn lại không được đánh lại số. Không được xóa riêng instance cuối cùng.

### BR27 — Reminder Uniqueness and Missed Trigger
Trong cùng Activity Instance, không cho phép hai Reminder có cùng `trigger_type` và `offset_minutes`, bất kể trạng thái enabled. Nếu thời điểm trigger đã qua, hệ thống bỏ qua và không gửi bù.

### BR28 — Schedule Composite Attribute
Schedule là nhóm ba thuộc tính bắt buộc trên Activity Instance, không phải entity/bảng riêng. `end_time` phải lớn hơn `start_time`; hoạt động qua nửa đêm nằm ngoài MVP.

### BR29 — Supported Recurrence Patterns
MVP chỉ hỗ trợ DAILY (mỗi N ngày) và WEEKLY (các ngày trong tuần đã chọn, mỗi N tuần). Khoảng ngày bao gồm hai đầu mút và không quá một năm; với WEEKLY, weekday của `start_date` phải nằm trong `days_of_week`.

### BR30 — Individual Activity Instance Deletion
Người dùng có thể xóa một Activity Instance riêng lẻ sau khi xác nhận nếu Activity còn ít nhất một instance khác. Reminder phụ thuộc instance bị xóa theo; các `series_position` còn lại giữ nguyên và không tạo occurrence bù. Không được xóa instance cuối cùng riêng lẻ; phải xóa Activity cha.

## 4. Traceability

### 4.1 User Need → Requirements → Use Cases → Domain

| User Need | FR/NFR chính | Use Cases | Domain / data |
|---|---|---|---|
| UN01 — Nhận biết kế hoạch | FR01, FR02, FR16, FR16.1; NFR05 | UC03, UC04, UC05 | Activity Instance, Schedule, Priority |
| UN02 — Sắp xếp hoạt động | FR03, FR04.1, FR06, FR06.1; Phase 2: FR10–FR13 | UC01, UC02, UC05, UC08 | Activity, Activity Instance, Priority, Activity Tag/Subject/Location (Phase 2) |
| UN03 — Lập kế hoạch | FR03–FR05, FR07, FR09, FR09.1 | UC01, UC02 | Activity, Recurrence, Activity Instance, Schedule, Deadline |
| UN04 — Theo dõi tiến độ | FR14, FR15; NFR02 | UC06, UC07 | Activity Instance.Status |
| UN05 — Không bỏ sót hoạt động | FR07, FR08, FR08.1; NFR04 | UC01, UC02, UC09 | Activity Instance.Deadline, Schedule, Reminder |
| UN02 — Sắp xếp hoạt động | FR18 | UC11 | Activity Instance, composite identity, dependent Reminder |
| UN06 — Tính ổn định | FR17, FR18; NFR01, NFR02, NFR03, NFR04, NFR06 | UC10, UC11 and all core use cases | Constraints, transactions, cascade delete, validation, error handling |
| UN07 — Trải nghiệm sử dụng | NFR03, NFR05 | UC01–UC11 where applicable | UI flow, clear labels, responsive feedback |

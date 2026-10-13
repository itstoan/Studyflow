# UC01 — Create Activity / Fixed Recurrence Batch

## 1. General Information

**Use Case ID:** UC01  
**Use Case Name:** Create Activity / Fixed Recurrence Batch  
**Primary Actor:** User

## 2. Goal

Tạo một Activity và một Activity Instance nếu không lặp, hoặc tạo toàn bộ Activity Instance trong một Fixed Recurrence Batch nếu có lặp.

## 3. Trigger

Người dùng chọn chức năng tạo Activity mới.

## 4. Preconditions

- StudyFlow đang hoạt động.
- Người dùng có thể truy cập ứng dụng.

## 5. Postconditions

### Success

- Activity được lưu thành công.
- Mỗi Activity Instance có đủ ba thuộc tính Schedule hợp lệ (`schedule_date`, `start_time`, `end_time`) lưu trực tiếp trên instance; Schedule không phải entity/bảng riêng.
- Nếu không lặp, có đúng một Activity Instance. Nếu lặp, tất cả instance trong khoảng Recurrence đã chọn được tạo thành một batch hữu hạn, tối đa một năm.
- Deadline là tùy chọn ở từng Activity Instance. Trong batch lặp, Deadline mặc định để trống trên các instance; người dùng có thể thiết lập sau cho từng instance hoặc dùng thao tác bulk edit đủ điều kiện.
- Reminder theo Schedule được áp dụng riêng cho từng instance trong batch. Reminder theo Deadline chỉ được tạo khi instance tương ứng có Deadline. Không được tạo hai Reminder cùng instance có cùng loại trigger và offset; Reminder đã quá thời điểm kích hoạt sẽ bị bỏ qua, không gửi bù.

### Failure / Cancellation

- Không tạo Activity/instance nếu thiếu Schedule hoặc dữ liệu bắt buộc không hợp lệ.
- Nếu việc tạo batch thất bại, hệ thống không để lại một Activity được tạo dở dang mà thiếu instance/Schedule bắt buộc.
- Nếu người dùng hủy, các thay đổi chưa lưu bị loại bỏ.

## 6. Main Flow

1. Người dùng chọn Create Activity.
2. Hệ thống hiển thị form Activity và Schedule cho lần diễn ra đầu tiên.
3. Người dùng nhập Name (không bắt buộc), Description (không bắt buộc) và Priority mặc định.
4. Người dùng nhập Schedule ban đầu gồm ngày, giờ bắt đầu và giờ kết thúc. Với batch lặp, ngày bắt đầu là occurrence đầu tiên; giờ bắt đầu/kết thúc được sao chép cho từng ngày occurrence.
5. Với hoạt động không lặp, người dùng có thể thiết lập Deadline trong form. Với batch lặp, Deadline của mỗi instance mặc định để trống và có thể được thiết lập sau khi tạo.
6. Người dùng có thể thiết lập Reminder trước Schedule bằng một khoảng thời gian tương đối. Nếu tạo batch lặp, cùng offset Reminder theo Schedule được áp dụng riêng cho từng instance. Reminder theo Deadline chỉ được tạo cho instance có Deadline. Người dùng có thể tạo nhiều Reminder khác offset hoặc khác loại trigger, nhưng không thể tạo cấu hình trùng `(trigger_type, offset_minutes)` trên cùng instance.
7. Người dùng có thể chọn DAILY (mỗi N ngày) hoặc WEEKLY (một/nhiều ngày trong tuần, mỗi N tuần) và ngày kết thúc, không vượt quá một năm từ ngày bắt đầu. Với WEEKLY, ngày bắt đầu phải thuộc tập ngày được chọn.
8. Người dùng xác nhận tạo Activity.
9. Hệ thống kiểm tra dữ liệu Activity, Schedule, Recurrence, Deadline và Reminder.
10. Hệ thống xác định các lần diễn ra trong batch nếu có Recurrence.
11. Hệ thống kiểm tra Schedule conflicts; nếu có, cảnh báo người dùng.
12. Sau khi validation được chấp nhận, hệ thống lưu Activity, Recurrence nếu có, từng Activity Instance và Reminder tương ứng trong một transaction nhất quán. Schedule nằm trực tiếp trên Activity Instance.
13. Hệ thống thông báo tạo thành công và các instance có thể xuất hiện trên lịch ngay lập tức.

## 7. Alternative Flows

### A1 — Thiếu Schedule hoặc Schedule không hợp lệ

1. Hệ thống phát hiện thiếu ngày/giờ hoặc giờ kết thúc không hợp lệ.
2. Hệ thống hiển thị lỗi và giữ nguyên form.
3. Người dùng sửa dữ liệu hoặc hủy thao tác. Không lưu dữ liệu không hợp lệ.

### A2 — Schedule conflict

1. Hệ thống phát hiện Schedule giao nhau với Schedule của Activity Instance khác.
2. Hệ thống cảnh báo người dùng.
3. Người dùng sửa Schedule hoặc xác nhận bỏ qua cảnh báo.
4. Nếu sửa, hệ thống kiểm tra lại; nếu xác nhận bỏ qua, hệ thống tiếp tục lưu.

### A3 — Recurrence không hợp lệ

1. Hệ thống phát hiện khoảng Recurrence vượt quá một năm hoặc cấu hình không hợp lệ.
2. Hệ thống báo lỗi và giữ form.
3. Người dùng sửa Recurrence hoặc hủy thao tác.

### A4 — Reminder dựa trên Deadline nhưng không có Deadline

1. Hệ thống phát hiện Reminder kiểu DEADLINE nhưng instance tương ứng không có Deadline.
2. Hệ thống yêu cầu loại bỏ cấu hình Reminder đó hoặc thiết lập Deadline hợp lệ cho instance phù hợp.

### A5 — Người dùng hủy

1. Người dùng chọn Cancel.
2. Hệ thống đóng form mà không lưu Activity/instance mới.

## 8. Related Functional Requirements

- FR03 — Tạo Activity và Activity Instance
- FR05 — Thiết lập Schedule
- FR06 — Thiết lập Priority
- FR07 — Thiết lập Deadline
- FR08 — Thiết lập Reminder
- FR09 — Thiết lập Recurrence khi tạo
- FR09.1 — Tạo Fixed Recurrence Batch
- FR10–FR13 — Chức năng Phase 2 khi được triển khai

## 9. Related Business Rules

- BR02 — Activity Instance Scheduling
- BR03 — Activity–Instance Relationship
- BR05 — Optional Deadline per Instance
- BR06 — Reminder per Instance
- BR10 — Recurrence Limit and Fixed Batch
- BR12 — Activity Name Optional
- BR20 — Initialize Instance Values
- BR21 — Schedule Conflict

# UC02 — Edit Activity Definition or Activity Instance

## 1. General Information

**Use Case ID:** UC02  
**Use Case Name:** Edit Activity Definition or Activity Instance  
**Primary Actor:** User

## 2. Goal

Cho phép người dùng chỉnh sửa metadata của Activity cha hoặc chỉnh sửa dữ liệu thực tế của một Activity Instance mà không vô tình thay đổi instance khác.

## 3. Trigger

Người dùng chọn Activity hoặc Activity Instance và yêu cầu chỉnh sửa.

## 4. Preconditions

- Đối tượng cần chỉnh sửa đã tồn tại.
- StudyFlow đang hoạt động.

## 5. Postconditions

### Success

- Nếu chỉnh sửa Activity definition, chỉ metadata của Activity được thay đổi; các Activity Instance đã tồn tại không tự động cập nhật. Recurrence đã dùng để tạo batch không thể chỉnh sửa.
- Nếu chỉnh sửa một Activity Instance, chỉ dữ liệu trong phạm vi được chọn được cập nhật.
- Nếu người dùng chọn áp dụng thuộc tính đã thay đổi cho instance được chọn và các instance tương lai đủ điều kiện, hệ thống cập nhật các instance đã tồn tại trong cùng batch; không tạo thêm hoặc xóa instance.
- Instance đã diễn ra trong quá khứ hoặc có Status Completed không bị bulk update.
- Khi thay đổi Schedule riêng cho một instance, hệ thống đánh dấu `schedule_exception = true`.

### Failure / Cancellation

- Không lưu nếu dữ liệu hoặc Schedule không hợp lệ.
- Nếu hủy, dữ liệu trước chỉnh sửa được giữ nguyên.

## 6. Main Flow

1. Người dùng chọn Activity hoặc Activity Instance.
2. Hệ thống hiển thị thông tin hiện tại.
3. Nếu là Activity, người dùng có thể chỉnh sửa metadata được hỗ trợ; không thể chỉnh sửa Recurrence sau khi batch đã tạo.
4. Nếu là Activity Instance, người dùng chỉnh sửa Name, Description, các trường Schedule (`schedule_date`, `start_time`, `end_time`), Priority, Deadline, Reminder và các trường Phase 2 khi có hỗ trợ. Status được cập nhật qua UC06.
5. Nếu instance thuộc Fixed Recurrence Batch, hệ thống cho phép chọn “Chỉ instance này” hoặc “Instance này và các instance tương lai chưa hoàn thành”. Lựa chọn bulk chỉ khả dụng khi instance được chọn ở tương lai và chưa Completed.
6. Hệ thống kiểm tra dữ liệu, Reminder/Deadline consistency và Schedule conflict.
7. Nếu phạm vi là một instance, hệ thống chỉ cập nhật instance đó. Nếu là bulk update, hệ thống chỉ cập nhật các thuộc tính nằm trong thay đổi cho các instance đủ điều kiện dựa trên `series_position`.
8. Với bulk Schedule edit, chỉ đồng bộ `start_time`/`end_time` trong khi giữ nguyên `schedule_date` của từng instance; thay đổi ngày áp dụng riêng cho instance được chọn. Schedule exception được giữ nguyên khi bulk update Schedule.
9. Hệ thống lưu thay đổi như một thao tác nhất quán và phản ánh kết quả.

## 7. Alternative Flows

### A1 — Dữ liệu hoặc Schedule không hợp lệ

1. Hệ thống thông báo lỗi và giữ form.
2. Không lưu thay đổi không hợp lệ.

### A2 — Schedule conflict

1. Hệ thống cảnh báo về Schedule giao nhau.
2. Người dùng sửa Schedule hoặc xác nhận bỏ qua cảnh báo.
3. Hệ thống kiểm tra lại nếu Schedule đã được sửa.

### A3 — Chỉ chỉnh sửa instance được chọn

1. Người dùng chọn “Chỉ instance này”.
2. Hệ thống chỉ cập nhật instance đó.
3. Nếu bất kỳ thuộc tính Schedule nào thay đổi riêng (`schedule_date`, `start_time`, `end_time`), hệ thống đặt `schedule_exception = true`.
4. Các instance khác và Activity cha không tự động thay đổi.

### A4 — Áp dụng thuộc tính cho instance tương lai đủ điều kiện

1. Người dùng chọn bulk update.
2. Hệ thống chọn các instance cùng Activity có `series_position` bằng hoặc lớn hơn instance được chọn, Schedule còn ở tương lai và Status chưa Completed.
3. Hệ thống cập nhật chỉ các thuộc tính đã thay đổi; bỏ qua instance quá khứ, instance Completed và giữ Schedule ngoại lệ khi thuộc tính được cập nhật là Schedule.
4. Hệ thống không sinh thêm, xóa hoặc tái tạo instance.

### A5 — Hủy thao tác

1. Người dùng hủy form.
2. Hệ thống loại bỏ thay đổi chưa lưu và giữ dữ liệu cũ.

## 8. Related Functional Requirements

- FR04 — Chỉnh sửa Activity Definition
- FR04.1 — Chỉnh sửa Activity Instance
- FR05 — Thiết lập Schedule
- FR06 — Thiết lập Priority
- FR07 — Thiết lập Deadline
- FR08 — Thiết lập Reminder
- FR10–FR13 — Chức năng Phase 2 khi được triển khai

## 9. Related Business Rules

- BR03 — Activity–Instance Relationship
- BR04 — Instance Status
- BR05 — Optional Deadline per Instance
- BR06 — Reminder per Instance
- BR11 — Activity Instance Data Independence
- BR13 — Edit Instance Scope
- BR14 — Single-Instance Edit
- BR15 — Editing Activity Definition
- BR16 — Explicit Bulk Update
- BR17 — Schedule Exception
- BR18 — Recurrence Configuration Is Fixed After Creation
- BR19 — Protect Past and Completed Instances
- BR21 — Schedule Conflict
- BR23 — Bulk Update Eligibility
- BR24 — No Automatic Recurrence Regeneration

# UC03 — View Daily Plan

## 1. General Information

**Use Case ID:** UC03
**Use Case Name:** View Daily Plan
**Primary Actor:** User

## 2. Goal

Cho phép người dùng xem các Activity Instance được lên lịch trong một ngày cụ thể theo thứ tự thời gian.

## 3. Trigger

Người dùng mở chế độ xem theo ngày hoặc chọn một ngày cụ thể.

## 4. Preconditions

* Người dùng có quyền truy cập StudyFlow.
* Hệ thống đang hoạt động.

## 5. Postconditions

### Success

* Các Activity Instance được lên lịch trong ngày được hiển thị.
* Các Activity Instance được sắp xếp theo Schedule.

### Failure

* Nếu không có Activity trong ngày, hệ thống hiển thị trạng thái không có Activity.
* Nếu không thể tải dữ liệu, hệ thống thông báo lỗi.

## 6. Main Flow

1. Người dùng mở chế độ xem theo ngày.
2. Hệ thống xác định ngày cần hiển thị.
3. Hệ thống lấy các Activity Instance được lên lịch trong ngày.
4. Hệ thống sắp xếp các Activity Instance theo thời gian.
5. Hệ thống hiển thị danh sách Activity Instance cho người dùng.
6. Người dùng có thể xem thông tin của từng Activity Instance.

## 7. Alternative Flows

### A1 — Không có Activity

1. Hệ thống không tìm thấy Activity Instance nào trong ngày.
2. Hệ thống hiển thị trạng thái không có Activity được lên lịch.

### A2 — Không tải được dữ liệu

1. Hệ thống không thể lấy dữ liệu.
2. Hệ thống thông báo lỗi.
3. Người dùng có thể thực hiện lại thao tác.

## 8. Related Requirements

* FR02 — Xem hoạt động theo ngày

## 9. Related Business Rules

- BR02 — Activity Instance Scheduling
- BR07 — Daily Activity Ordering
# UC04 — View Weekly Plan

## 1. General Information

**Use Case ID:** UC04
**Use Case Name:** View Weekly Plan
**Primary Actor:** User

## 2. Goal

Cho phép người dùng xem toàn bộ Activity Instance được lên lịch trong một tuần.

## 3. Trigger

Người dùng chọn chế độ xem theo tuần hoặc chọn một tuần cụ thể.

## 4. Preconditions

* Người dùng có quyền truy cập StudyFlow.
* Hệ thống đang hoạt động.

## 5. Postconditions

### Success

* Các Activity Instance được lên lịch trong tuần được hiển thị.
* Schedule của từng Activity Instance được hiển thị.

### Failure

* Nếu không có Activity trong tuần, hệ thống hiển thị trạng thái không có Activity.
* Nếu không thể tải dữ liệu, hệ thống thông báo lỗi.

## 6. Main Flow

1. Người dùng mở chế độ xem theo tuần.
2. Hệ thống xác định tuần cần hiển thị.
3. Hệ thống lấy các Activity Instance thuộc tuần đó.
4. Hệ thống nhóm các Activity Instance theo ngày.
5. Hệ thống hiển thị kế hoạch của toàn bộ tuần.
6. Người dùng có thể chọn một Activity Instance để xem thông tin chi tiết.

## 7. Alternative Flows

### A1 — Không có Activity

1. Hệ thống không tìm thấy Activity Instance nào trong tuần.
2. Hệ thống hiển thị trạng thái không có Activity được lên kế hoạch.

### A2 — Không tải được dữ liệu

1. Hệ thống không thể lấy dữ liệu.
2. Hệ thống thông báo lỗi.
3. Người dùng có thể thực hiện lại thao tác.

## 8. Related Requirements

* FR01 — Xem kế hoạch tuần

## 9. Related Business Rules

- BR02 — Activity Instance Scheduling

# UC05 — View Upcoming Activities

## 1. General Information

**Use Case ID:** UC05
**Use Case Name:** View Upcoming Activities
**Primary Actor:** User

## 2. Goal

Cho phép người dùng xem các Activity Instance sắp diễn ra sau khi các Activity Instance cần xử lý trong ngày hiện tại đã kết thúc.

## 3. Trigger

Hệ thống xác định rằng các Activity Instance được lên lịch trong ngày hiện tại đã kết thúc và người dùng đang ở màn hình chính.

## 4. Preconditions

* Người dùng có quyền truy cập StudyFlow.
* Hệ thống đang hoạt động.

## 5. Postconditions

### Success

* Các Activity Instance sắp diễn ra được hiển thị.
* Các Activity được sắp xếp theo tiêu chí hiện tại.

### Failure

* Nếu không có Activity sắp diễn ra, hệ thống hiển thị trạng thái không có Activity sắp tới.
* Nếu không tải được dữ liệu, hệ thống thông báo lỗi.

## 6. Main Flow

1. Hệ thống xác định rằng các Activity Instance trong ngày hiện tại đã kết thúc.
2. Hệ thống tìm các Activity Instance sắp diễn ra trong tương lai.
3. Hệ thống áp dụng tiêu chí sắp xếp hiện tại.
4. Hệ thống hiển thị danh sách Upcoming Activities.
5. Người dùng có thể thay đổi tiêu chí sắp xếp hoặc áp dụng bộ lọc.

## 7. Alternative Flows

### A1 — Không có Upcoming Activity

1. Hệ thống không tìm thấy Activity Instance nào trong tương lai.
2. Hệ thống hiển thị trạng thái không có Activity sắp tới.

### A2 — Người dùng thay đổi tiêu chí sắp xếp

1. Người dùng chọn một tiêu chí sắp xếp khác.
2. Hệ thống sắp xếp lại danh sách.
3. Hệ thống hiển thị kết quả mới.

### A3 — Người dùng áp dụng bộ lọc

1. Người dùng chọn một hoặc nhiều điều kiện lọc.
2. Hệ thống lọc danh sách Activity Instance.
3. Hệ thống hiển thị kết quả sau khi lọc.

## 8. Related Requirements

* FR06.1 — Sắp xếp Activity Instance theo Priority
* FR16 — Xem Activity sắp diễn ra
* FR16.1 — Sắp xếp và lọc Activity Instance sắp diễn ra

## 9. Related Business Rules

- BR08 — Upcoming Activity Display
- BR09 — Upcoming Activity Ordering
# UC06 — Update Activity Instance Status

## 1. General Information

**Use Case ID:** UC06
**Use Case Name:** Update Activity Instance Status
**Primary Actor:** User

## 2. Goal

Cho phép người dùng cập nhật trạng thái của một Activity Instance theo tình trạng thực tế của lần diễn ra đó.

## 3. Trigger

Người dùng chọn một Activity Instance và thay đổi Status.

## 4. Preconditions

* Activity Instance tồn tại.
* Người dùng có quyền truy cập Activity Instance đó.

## 5. Postconditions

### Success

* Status của Activity Instance được cập nhật thành công.
* Các Activity Instance khác không bị thay đổi.

### Failure

* Status không được cập nhật nếu giá trị không hợp lệ.
* Dữ liệu cũ được giữ nguyên nếu cập nhật thất bại.

## 6. Main Flow

1. Người dùng chọn một Activity Instance.
2. Hệ thống hiển thị Status hiện tại.
3. Người dùng chọn Status mới: `NOT_STARTED`, `IN_PROGRESS` hoặc `COMPLETED`.
4. Người dùng xác nhận thay đổi.
5. Hệ thống kiểm tra Status.
6. Hệ thống cập nhật Status của Activity Instance.
7. Hệ thống lưu thay đổi.
8. Hệ thống hiển thị Status mới.

## 7. Alternative Flows

### A1 — Status không hợp lệ

1. Hệ thống phát hiện Status không thuộc `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`.
2. Hệ thống thông báo lỗi.
3. Status cũ được giữ nguyên.

## 8. Related Requirements

* FR14 — Cập nhật Status của Activity Instance

## 9. Related Business Rules

- BR04 — Instance Status
- BR11 — Activity Instance Data Independence
# UC07 — View Activity Progress

## 1. General Information

**Use Case ID:** UC07
**Use Case Name:** View Activity Progress
**Primary Actor:** User

## 2. Goal

Cho phép người dùng xem trạng thái và mức độ hoàn thành của các Activity Instance trong một khoảng thời gian.

## 3. Trigger

Người dùng yêu cầu xem tiến độ Activity.

## 4. Preconditions

* Người dùng có quyền truy cập StudyFlow.
* Hệ thống đang hoạt động.

## 5. Postconditions

### Success

* Hệ thống hiển thị thông tin trạng thái và mức độ hoàn thành của các Activity Instance trong khoảng thời gian được chọn.

## 6. Main Flow

1. Người dùng chọn khoảng thời gian cần xem.
2. Hệ thống lấy các Activity Instance thuộc khoảng thời gian đó.
3. Hệ thống xác định trạng thái của các Activity Instance.
4. Hệ thống tổng hợp thông tin hoàn thành.
5. Hệ thống hiển thị kết quả cho người dùng.

## 7. Alternative Flows

### A1 — Không có dữ liệu

1. Hệ thống không tìm thấy Activity Instance trong khoảng thời gian.
2. Hệ thống hiển thị trạng thái không có dữ liệu.

### A2 — Không tải được dữ liệu

1. Hệ thống không thể lấy dữ liệu.
2. Hệ thống thông báo lỗi.

## 8. Related Requirements

* FR15 — Xem trạng thái và tiến độ Activity

## 9. Related Business Rules

- BR04 — Instance Status
- BR11 — Activity Instance Data Independence
# UC08 — Filter Activities by Tag

## 1. General Information

**Use Case ID:** UC08
**Use Case Name:** Filter Activities by Tag
**Primary Actor:** User

## 2. Goal

Cho phép người dùng lọc Activity theo Tag; các Activity Instance được hiển thị theo Tag của Activity cha. Tag chỉ gắn tại cấp Activity.

## 3. Trigger

Người dùng chọn một hoặc nhiều Tag để lọc Activity và các instance thuộc Activity đó.

## 4. Preconditions

* Người dùng có quyền truy cập StudyFlow.
* Có Activity hoặc Activity Instance đã được gắn Tag.

## 5. Postconditions

### Success

* Hệ thống hiển thị các Activity hoặc Activity Instance phù hợp với điều kiện lọc.

## 6. Main Flow

1. Người dùng chọn chức năng lọc.
2. Hệ thống hiển thị các Tag có thể sử dụng.
3. Người dùng chọn Tag.
4. Hệ thống tìm các Activity có Tag tương ứng và hiển thị các instance thuộc những Activity đó.
5. Hệ thống hiển thị kết quả lọc.

## 7. Alternative Flows

### A1 — Không có Activity phù hợp

1. Hệ thống không tìm thấy Activity hoặc Activity Instance phù hợp với Tag.
2. Hệ thống hiển thị trạng thái không có kết quả.

### A2 — Người dùng bỏ lọc

1. Người dùng xóa điều kiện lọc.
2. Hệ thống hiển thị lại danh sách Activity ban đầu.

## 8. Related Requirements

* FR12 — Lọc Activity theo Tag

## 9. Related Business Rules

- BR22 — Tag Association (Phase 2)
# UC09 — Receive Reminder Notification

## 1. General Information

**Use Case ID:** UC09  
**Use Case Name:** Receive Reminder Notification  
**Primary Actor:** User

## 2. Goal

Hiển thị thông báo trong giao diện StudyFlow khi một Reminder đến hạn trong lúc trang StudyFlow đang mở.

## 3. Trigger

Frontend polling khi trang StudyFlow đang mở phát hiện Reminder có thời điểm kích hoạt đến hạn.

## 4. Preconditions

- Reminder tồn tại, enabled và hợp lệ.
- Trang StudyFlow đang mở; JavaScript chạy được và có kết nối tới backend.
- Reminder chưa được ghi nhận đã hiển thị.

## 5. Postconditions

### Success

- Người dùng nhìn thấy thông báo trong giao diện StudyFlow.
- Backend ghi nhận đã hiển thị (`sent_at`) để hạn chế hiển thị lặp.

### Failure / Limitation

- Nếu trang đóng, trình duyệt bị tạm ngưng hoặc thiết bị ngủ, frontend không bảo đảm kiểm tra Reminder đúng giờ.
- Nếu frontend bỏ lỡ trigger và thời điểm đó đã quá hạn khi kiểm tra lại, Reminder bị bỏ qua, không hiển thị bù.

## 6. Main Flow

1. Khi StudyFlow đang mở, frontend định kỳ gọi API để kiểm tra Reminder đến hạn.
2. Backend tính trigger time dựa trên Schedule hoặc Deadline của Activity Instance.
3. Backend chỉ trả các Reminder đến hạn trong khoảng kiểm tra hiện tại, enabled, chưa được ghi nhận đã hiển thị và vẫn hợp lệ.
4. Frontend hiển thị thông báo trong giao diện StudyFlow.
5. Frontend gửi xác nhận hiển thị tới backend; backend ghi nhận thời điểm xử lý để hạn chế hiển thị lặp.

## 7. Alternative Flows

### A1 — Reminder bị disabled hoặc không hợp lệ

1. Backend không trả Reminder đó về frontend.
2. Không hiển thị thông báo.

### A2 — Trigger đã quá hạn

1. Backend phát hiện thời điểm trigger đã quá khoảng kiểm tra được hỗ trợ.
2. Reminder bị bỏ qua; không gửi/hiển thị bù.

### A3 — Trang hoặc kết nối không hoạt động

1. Frontend không thể kiểm tra Reminder.
2. Không bảo đảm thông báo được hiển thị trong thời gian này.
3. Khi hoạt động trở lại, chỉ xử lý Reminder vẫn nằm trong khoảng kiểm tra hiện tại; không gửi bù các trigger đã qua.

## 8. Related Requirements

- FR08 — Thiết lập Reminder
- FR08.1 — Thông báo Reminder

## 9. Related Business Rules

- BR06 — Reminder per Instance
- BR27 — Reminder Uniqueness and Missed Trigger

## 10. MVP Limitations

- Chỉ hiển thị notification bên trong giao diện StudyFlow khi trang đang mở.
- Không triển khai browser push notification, service-worker push hoặc Reminder Worker riêng trong MVP.


# UC10 — Delete Activity and Cascade Dependents

## 1. General Information

**Use Case ID:** UC10  
**Use Case Name:** Delete Activity and Cascade Dependents  
**Primary Actor:** User

## 2. Goal

Cho phép người dùng xóa một Activity và toàn bộ dữ liệu phụ thuộc của nó theo đúng quan hệ cha–con.

## 3. Trigger

Người dùng chọn Delete trên một Activity.

## 4. Preconditions

- Activity tồn tại.
- Người dùng đang sử dụng StudyFlow riêng tư và có quyền thao tác trên dữ liệu.

## 5. Postconditions

### Success

- Activity bị xóa.
- Recurrence configuration (nếu có), tất cả Activity Instance của Activity đó và các Reminder phụ thuộc bị xóa theo.
- Các Activity và Reminder không liên quan không bị ảnh hưởng.

### Failure / Cancellation

- Nếu người dùng hủy xác nhận, không có dữ liệu nào bị xóa.
- Nếu xóa thất bại, thao tác phải được rollback; không để lại dữ liệu xóa dở dang.

## 6. Main Flow

1. Người dùng chọn Activity và yêu cầu xóa.
2. Hệ thống hiển thị cảnh báo rằng toàn bộ các instance và Reminder thuộc Activity sẽ bị xóa.
3. Người dùng xác nhận.
4. Hệ thống xóa Activity trong một transaction; các quan hệ phụ thuộc được xóa theo cascade.
5. Hệ thống xác nhận thao tác thành công và cập nhật các màn hình liên quan.

## 7. Alternative Flows

### A1 — Người dùng hủy

1. Người dùng không xác nhận hoặc chọn Cancel.
2. Hệ thống giữ nguyên Activity và tất cả dữ liệu phụ thuộc.

### A2 — Xóa thất bại

1. Hệ thống phát hiện lỗi khi xóa.
2. Hệ thống rollback transaction và thông báo lỗi.
3. Dữ liệu trước thao tác được giữ nguyên.

## 8. Related Functional Requirements

- FR17 — Xóa Activity

## 9. Related Business Rules

- BR03 — Activity–Instance Relationship
- BR26 — Activity Instance Identification and Cascade Delete


# UC11 — Delete Activity Instance

## 1. General Information

**Use Case ID:** UC11  
**Use Case Name:** Delete Activity Instance  
**Primary Actor:** User

## 2. Goal

Cho phép người dùng xóa một lần diễn ra riêng lẻ mà không xóa Activity cha hoặc các instance khác.

## 3. Trigger

Người dùng chọn Delete trên một Activity Instance.

## 4. Preconditions

- Activity Instance tồn tại.
- Activity cha đang có ít nhất hai Activity Instance trước thao tác.

## 5. Postconditions

### Success

- Activity Instance được chọn bị xóa.
- Reminder phụ thuộc instance đó bị xóa theo.
- Activity cha và các instance còn lại vẫn tồn tại.
- `series_position` của các instance còn lại không thay đổi; không tạo occurrence bù.

### Failure / Cancellation

- Nếu đây là instance cuối cùng của Activity, hệ thống từ chối xóa riêng và hướng người dùng sang UC10 để xóa Activity cha.
- Nếu người dùng hủy xác nhận, dữ liệu được giữ nguyên.
- Nếu xóa thất bại, transaction được rollback.

## 6. Main Flow

1. Người dùng chọn một Activity Instance và yêu cầu xóa.
2. Hệ thống xác nhận Activity cha còn ít nhất hai instance.
3. Hệ thống hiển thị cảnh báo rằng instance và các Reminder của nó sẽ bị xóa.
4. Người dùng xác nhận.
5. Hệ thống xóa Activity Instance; các Reminder liên quan bị xóa theo cascade.
6. Hệ thống giữ nguyên `series_position` của các instance còn lại và cập nhật các màn hình liên quan.
7. Hệ thống thông báo xóa thành công.

## 7. Alternative Flows

### A1 — Đây là instance cuối cùng

1. Hệ thống phát hiện Activity chỉ còn một instance.
2. Hệ thống không cho xóa riêng instance.
3. Hệ thống đề nghị người dùng dùng UC10 để xóa Activity cha cùng dữ liệu phụ thuộc.

### A2 — Người dùng hủy

1. Người dùng hủy xác nhận.
2. Hệ thống giữ nguyên Activity Instance và Reminder.

### A3 — Xóa thất bại

1. Hệ thống phát hiện lỗi.
2. Hệ thống rollback transaction và thông báo lỗi.

## 8. Related Functional Requirements

- FR18 — Xóa Activity Instance

## 9. Related Business Rules

- BR03 — Activity–Instance Relationship
- BR26 — Activity Instance Identification and Cascade Delete
- BR30 — Individual Activity Instance Deletion

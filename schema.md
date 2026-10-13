# Relational Schema — StudyFlow (locked design baseline)

**Scope:** MVP là ứng dụng riêng tư cho một người dùng. Các bảng Subject/Tag/Location là Phase 2. Schema này là thiết kế quan hệ trước khi viết DDL cụ thể.

## ACTIVITY

```text
ACTIVITY
--------
id                  PK
name                NULL
description          NULL
default_priority    NOT NULL CHECK IN (LOW, MEDIUM, HIGH)
subject_id          FK NULL       -- Phase 2 default Subject
default_location     NULL          -- Phase 2 default Location
```

`Activity` là entity cha. `name`/`description` có thể NULL. `default_priority` bắt buộc. Các default chỉ được sao chép khi tạo batch; thay đổi Activity không cập nhật instance đã có.

## RECURRENCE

```text
RECURRENCE
----------
id                  PK
activity_id         FK UNIQUE NOT NULL ON DELETE CASCADE
pattern             NOT NULL CHECK IN (DAILY, WEEKLY)
interval            NOT NULL CHECK (> 0)
days_of_week        REQUIRED for WEEKLY; NULL for DAILY
start_date          NOT NULL
end_date            NOT NULL
```

Một Activity có tối đa một Recurrence. Hai ngày đầu/cuối được tính bao gồm; `end_date >= start_date`, thời gian batch không quá một năm. Với `WEEKLY`, `days_of_week` là tập các ngày trong tuần và phải chứa weekday của `start_date`; `interval` là chu kỳ mỗi N tuần. Với `DAILY`, `interval` là số ngày giữa các occurrence và `days_of_week` phải NULL. Lưu ý: biểu diễn vật lý của tập `days_of_week` sẽ được chốt khi chọn dialect/DDL; logic nghiệp vụ không cho phép giá trị trùng.

## ACTIVITY_INSTANCE — weak entity

```text
ACTIVITY_INSTANCE
-----------------
activity_id             PK, FK NOT NULL -> ACTIVITY.id ON DELETE CASCADE
series_position         PK NOT NULL
name                    NULL
description            NULL
priority                NOT NULL CHECK IN (LOW, MEDIUM, HIGH)
status                  NOT NULL CHECK IN (NOT_STARTED, IN_PROGRESS, COMPLETED)
schedule_date           NOT NULL
start_time              NOT NULL
end_time                NOT NULL
deadline_at            NULL
schedule_exception      NOT NULL DEFAULT FALSE
subject_id              FK NULL    -- Phase 2 instance-level override
location                NULL       -- Phase 2 actual Location
```

Khóa chính ghép `(activity_id, series_position)` thay thế cột `id`. `series_position` là partial key, bắt đầu từ 1, tăng theo thứ tự ngày occurrence tại thời điểm tạo batch và bất biến. Nếu instance bị xóa thủ công, không đánh lại số các vị trí còn lại; có thể có khoảng trống. Đây là cách thể hiện weak entity về mặt định danh; cascade delete vẫn cần khai báo rõ. `schedule_date`, `start_time`, `end_time` là ba cột tạo thành thuộc tính tổng hợp Schedule; không có bảng SCHEDULE.

Constraints/validation:

- `CHECK (end_time > start_time)`; sự kiện qua nửa đêm không nằm trong MVP.
- `schedule_date`, `start_time`, `end_time` đều NOT NULL, do đó một row instance luôn có đủ Schedule.
- `UNIQUE` không cần bổ sung cho `(activity_id, series_position)` vì đây là PK.
- Một Activity được lưu thành công phải có ít nhất một instance; bảo đảm ở service/transaction vì FK không tự bảo đảm quan hệ 1:N bắt buộc.

## REMINDER

```text
REMINDER
--------
id                  PK
activity_id         FK NOT NULL
series_position     FK NOT NULL
trigger_type        NOT NULL CHECK IN (SCHEDULE, DEADLINE)
offset_minutes      NOT NULL CHECK (offset_minutes >= 0)
enabled             NOT NULL DEFAULT TRUE
sent_at             NULL
```

`(activity_id, series_position)` là composite FK đến `ACTIVITY_INSTANCE` với `ON DELETE CASCADE`. `sent_at` ghi nhận Reminder đã gửi thành công để tránh gửi lặp. Một instance có thể có nhiều Reminder.

Constraints/validation:

- `UNIQUE(activity_id, series_position, trigger_type, offset_minutes)` ngăn cấu hình trùng, kể cả Reminder disabled.
- `trigger_type = DEADLINE` yêu cầu Activity Instance tương ứng có `deadline_at IS NOT NULL`; đây là ràng buộc liên bảng nên cần service validation hoặc DB trigger.
- Khi xóa Deadline, xóa Reminder có `trigger_type = DEADLINE` của instance đó.
- Nếu trigger time đã qua mà chưa gửi, không gửi bù. Trigger time được tính động: Schedule bắt đầu trừ offset hoặc Deadline trừ offset.
- Khi tạo batch lặp, Reminder theo Schedule được nhân ra thành cấu hình riêng cho mỗi instance. Reminder theo Deadline chỉ được thêm sau cho instance có Deadline.

## SUBJECT (Phase 2)

```text
SUBJECT
-------
id                  PK
name                NOT NULL
term                NULL
```

`ACTIVITY.subject_id` là Subject mặc định; `ACTIVITY_INSTANCE.subject_id` chỉ dùng khi sản phẩm cần override riêng cho instance.

## TAG and ACTIVITY_TAG (Phase 2)

```text
TAG
---
id                  PK
name                NOT NULL UNIQUE

ACTIVITY_TAG
------------
activity_id         PK, FK -> ACTIVITY.id ON DELETE CASCADE
tag_id              PK, FK -> TAG.id ON DELETE CASCADE
```

Tag chỉ gắn với Activity. Lọc instance theo Tag được thực hiện thông qua Activity cha. Không tạo `INSTANCE_TAG` trong thiết kế đã chốt.

## Delete rules

- Xóa `ACTIVITY` sẽ cascade xóa `RECURRENCE`, các `ACTIVITY_INSTANCE`, và qua composite FK xóa các `REMINDER`; `ACTIVITY_TAG` cũng cascade trong Phase 2.
- Xóa Activity sẽ cascade xóa Recurrence, toàn bộ Activity Instance và Reminder phụ thuộc.
- Có thể xóa riêng một Activity Instance nếu Activity còn ít nhất một instance khác sau thao tác; Reminder của instance đó cascade. Không đánh lại số `series_position` và không tạo occurrence bù.
- Không cho xóa riêng instance cuối cùng của Activity; người dùng phải xóa Activity cha để xóa toàn bộ batch.
- Khi xóa một Reminder hoặc Tag association riêng lẻ, chỉ bản ghi được chọn bị xóa.

## Data integrity / transactions

- Tạo Activity + Recurrence (nếu có) + tất cả Activity Instance + Reminder tương ứng trong một transaction. Không để lại Activity dở dang nếu tạo batch thất bại.
- Với hoạt động một lần: một instance có `series_position = 1`, không có Recurrence.
- Với hoạt động lặp: toàn bộ occurrence trong batch được tạo ngay, theo DAILY hoặc WEEKLY, giới hạn một năm.
- `status` là một trong ba giá trị đã chốt; không tự động đổi khi Schedule đã qua.
- `priority` là một trong ba mức đã chốt; sắp xếp mặc định HIGH → MEDIUM → LOW, sau đó theo Schedule.
- Schedule Conflict là cảnh báo, không phải từ chối tuyệt đối. Người dùng có thể sửa hoặc xác nhận bỏ qua. Kiểm tra trùng theo khoảng thời gian nửa mở `[start, end)`.
- Bulk edit không thêm/xóa instance; chỉ cập nhật instance đủ điều kiện, giữ nguyên instance quá khứ/Completed; chỉ thay thuộc tính người dùng đã chọn.

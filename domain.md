# Domain

## Subjects

Là các môn học có trong thời khoá biểu hiện tại trên trường.

### Ví dụ

* PPL
* DSA

## Activities

Một công việc, hoạt động hoặc sự kiện mà tôi muốn thực hiện và theo dõi.

### Ví dụ

* Làm PPL Assignment
* Làm project
* Đi tập thể thao
* Đi làm
* Đi chơi

## Schedules

Thời gian và ngày giờ cụ thể mà một hoạt động dự kiến hoặc được lên lịch để diễn ra.

### Ví dụ

* Học PPL vào thứ 2, 13:30–15:30
* Tập gym vào thứ 4, 18:00–19:00

## Reminders

Lời nhắc được thiết lập để thông báo cho người dùng trước một thời điểm hoặc sự kiện liên quan đến Activity, chẳng hạn như Schedule hoặc Deadline.

### Ví dụ

* Nhắc trước giờ học PPL 15 phút
* Nhắc trước deadline assignment 1 ngày

## Deadlines

Thời điểm cuối cùng mà một Activity cần được hoàn thành.

### Ví dụ

* PPL Assignment: 10/10/2026 23:59
* Project: 20/10/2026 23:59

## Status

Trạng thái thể hiện tình trạng hoàn thành của một Activity Occurrence.

### Ví dụ

* TODO
* IN_PROGRESS
* COMPLETED
* CANCELLED

## Relationships

### Subject → Activity

Một Subject có thể có các Activity liên quan đến môn học đó, chẳng hạn như assignment, project hoặc exam.

Một Activity có thể thuộc về một Subject hoặc không thuộc Subject nào nếu đó là hoạt động cá nhân.

### Activity → Schedule

Một Activity có thể được lên lịch một lần hoặc theo một quy tắc lặp lại.

Schedule xác định thời gian mà Activity dự kiến được thực hiện hoặc diễn ra.

### Activity → Deadline

Một Activity có thể có một Deadline, là thời điểm cuối cùng mà Activity cần được hoàn thành.

### Activity → Reminder

Một Activity có thể có một hoặc nhiều Reminder để nhắc người dùng về thời gian hoặc thời hạn liên quan đến Activity.

### Activity → Activity Occurrence

Một Activity có thể tạo ra một hoặc nhiều Activity Occurrence.

Mỗi Activity Occurrence đại diện cho một lần cụ thể mà Activity được lên lịch để diễn ra.

### Activity Occurrence → Status

Mỗi Activity Occurrence có một trạng thái riêng và được quản lý độc lập với các Occurrence khác của cùng Activity.

## Activity Occurrence

Một Activity có thể được lên lịch một lần hoặc lặp lại theo một quy tắc nhất định.

Mỗi lần diễn ra cụ thể của Activity được xem là một Activity Occurrence và được quản lý độc lập.

Ví dụ, với Activity "Đi gym" được lặp lại vào thứ 2, 4 và 6, mỗi buổi gym là một Activity Occurrence riêng biệt.

Trạng thái hoàn thành được quản lý cho từng Activity Occurrence, do đó việc hoàn thành một lần diễn ra không làm các lần diễn ra khác được đánh dấu hoàn thành.

### Example

Activity: Đi gym

* Thứ 2 → COMPLETED
* Thứ 4 → TODO
* Thứ 6 → TODO

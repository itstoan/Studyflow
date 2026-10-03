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

Lời nhắc được đặt để thông báo cho tôi về sự xảy ra của một sự kiện hoặc hoạt động khi cần thiết.

### Ví dụ

* Nhắc trước giờ học PPL 15 phút
* Nhắc trước deadline assignment 1 ngày

## Progress / Status

Trạng thái thể hiện mức độ hoàn thành của một hoạt động.

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

Một Activity có thể được lên lịch vào một hoặc nhiều khoảng thời gian cụ thể.

Schedule xác định thời gian mà Activity dự kiến được thực hiện hoặc diễn ra.

### Activity → Reminder

Một Activity có thể có một hoặc nhiều Reminder để nhắc người dùng về thời gian hoặc thời hạn liên quan đến Activity đó.

### Activity → Progress / Status

Mỗi Activity có một trạng thái hiện tại thể hiện mức độ hoàn thành của Activity.

Ví dụ:

* TODO
* IN_PROGRESS
* COMPLETED
* CANCELLED
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

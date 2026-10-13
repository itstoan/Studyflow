# Scope — StudyFlow

## MVP

MVP is a private, single-user personal activity-management web application. It does not require multi-user accounts while it remains privately accessible.

- Create an Activity and its Activity Instance(s).
- Model Schedule as three required attributes on Activity Instance: `schedule_date`, `start_time`, `end_time`; no separate Schedule table/entity.
- Create one-time activities or a fixed recurrence batch whose span is no more than one year.
- Support recurrence patterns DAILY and WEEKLY only.
- Generate the full batch at successful creation; do not automatically extend, regenerate or restructure it later.
- Use `Activity Instance` as a weak entity with composite key `(activity_id, series_position)`.
- View daily and weekly plans.
- View upcoming activities: daily entries appear chronologically; after today's scheduled activities have ended, show upcoming activities ordered by Priority then Schedule by default.
- Edit an Activity Instance individually or explicitly apply changed attributes to selected and subsequent eligible existing instances in the same batch.
- Set Priority (`LOW`, `MEDIUM`, `HIGH`), optional Deadline, and Reminder at Activity Instance level.
- Support multiple reminders before Schedule and/or Deadline; disallow duplicate Reminder configurations for the same instance, trigger type and offset.
- Display Reminder notifications inside StudyFlow only while the StudyFlow page is open and its frontend is running.
- Skip Reminder triggers missed while the page is closed/suspended; do not notify retroactively.
- Do not implement browser push notification or a dedicated background Reminder Worker in MVP.
- Update Status independently (`NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`) for each instance.
- View activity progress and completed-instance counts.
- Preserve past and Completed instances during bulk edits.
- Delete an individual Activity Instance with confirmation when its Activity will still have at least one other instance; its Reminders are deleted with it. Remaining `series_position` values are never renumbered.
- Delete an Activity with confirmation; Recurrence, all Activity Instances and dependent Reminders are deleted by cascade. If only one instance remains, delete the parent Activity instead of deleting that last instance separately.

### Recurrence limitations in MVP

- Recurrence is configured only when creating an Activity/batch.
- DAILY means every N days; WEEKLY means on selected weekday(s), every N weeks.
- The recurrence range includes start and end dates, spans at most one year, and for WEEKLY the start date must be one of the selected weekdays.
- Once created, recurrence configuration is not used to add, remove or regenerate instances.
- To create another period or a different pattern, create a new Activity. Copying settings may be added later as a convenience.
- Bulk edits never change the number of instances in a batch.

## Phase 2

- Assign default Subject to Activity and optionally override per instance.
- Add and manage Tags associated with Activity only; filter Activity and its instances through the parent Activity's Tags.
- Add Location, with default and instance-specific values.
- Improve activity organization and filtering.

Phase 2 fields must not be treated as required inputs in MVP flows. `INSTANCE_TAG` is not part of the agreed Phase 2 baseline.

## Future

### Notification enhancements

- Browser push notification or background Reminder delivery after MVP, if needed. The MVP does not notify when the StudyFlow page is closed.

### Public deployment / multi-user personalization

Before public deployment, add and verify authentication, authorization, secure configuration, and protection against unauthorized access. Multi-user support additionally requires per-user data ownership/isolation and preferences. These are not MVP features while the app remains private.

### Activity data storage

- Notes, files, resources, links, questions, and other information associated with Activity or Activity Instance.

### Potential recurrence enhancements

- Tools to copy an Activity into a new batch, extend a series, or support richer recurrence editing may be considered only after MVP is stable.

## Out of Scope for MVP

- AI-based planning or recommendations.
- Complex real-time collaboration.
- Payments or financial features.
- Microservices/Kubernetes architecture.
- A dedicated mobile application.
- Advanced external-service integrations.
- Automatically synchronizing/rebuilding an existing recurrence batch after the recurrence rule changes.
- Publicly exposing the MVP without the appropriate access/security controls.

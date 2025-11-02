# HR and Education SQL Patterns

This reference provides common SQL patterns specifically tailored for educational human resources databases. These patterns address the unique challenges of managing employee records, credentials, student data, course enrollments, and organizational hierarchies in educational institutions.

## Table of Contents

1. [Employee Management Patterns](#employee-management-patterns)
2. [Credential Tracking and Verification](#credential-tracking-and-verification)
3. [Department and Organization Patterns](#department-and-organization-patterns)
4. [Student Enrollment Patterns](#student-enrollment-patterns)
5. [Course and Schedule Management](#course-and-schedule-management)
6. [Leave and Absence Tracking](#leave-and-absence-tracking)
7. [Payroll and Compensation Patterns](#payroll-and-compensation-patterns)
8. [Reporting and Analytics Patterns](#reporting-and-analytics-patterns)

---

## Employee Management Patterns

### Pattern 1: Active Employee Roster with Current Status

**Use Case**: Generate a current roster of all active employees with their primary assignment and contact information.

```sql
WITH CurrentAssignments AS (
    SELECT
        employee_id,
        department_id,
        job_title,
        assignment_start_date,
        ROW_NUMBER() OVER (
            PARTITION BY employee_id
            ORDER BY assignment_start_date DESC
        ) as rn
    FROM employee_assignments
    WHERE assignment_end_date IS NULL
       OR assignment_end_date > GETDATE()
)
SELECT
    e.employee_id,
    e.first_name + ' ' + e.last_name AS full_name,
    e.email,
    e.phone,
    e.hire_date,
    DATEDIFF(YEAR, e.hire_date, GETDATE()) AS years_of_service,
    ca.job_title,
    d.department_name,
    d.school_site
FROM employees e
INNER JOIN CurrentAssignments ca ON e.employee_id = ca.employee_id AND ca.rn = 1
INNER JOIN departments d ON ca.department_id = d.department_id
WHERE e.status = 'Active'
ORDER BY d.school_site, d.department_name, e.last_name;
```

**Key Features**:
- Uses ROW_NUMBER to handle employees with multiple concurrent assignments
- Calculates years of service for seniority tracking
- Includes NULL-safe date filtering for open-ended assignments

### Pattern 2: Employee Change History Tracking

**Use Case**: Track all changes to employee records for compliance and audit purposes.

```sql
-- Create change tracking table
CREATE TABLE employee_change_history (
    change_id INT IDENTITY(1,1) PRIMARY KEY,
    employee_id INT NOT NULL,
    field_name NVARCHAR(100) NOT NULL,
    old_value NVARCHAR(MAX),
    new_value NVARCHAR(MAX),
    change_date DATETIME DEFAULT GETDATE(),
    changed_by NVARCHAR(100) DEFAULT SYSTEM_USER,
    change_reason NVARCHAR(500)
);

-- Trigger to capture changes
CREATE TRIGGER trg_employee_changes
ON employees
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Capture salary changes
    INSERT INTO employee_change_history (employee_id, field_name, old_value, new_value, change_reason)
    SELECT
        i.employee_id,
        'salary',
        CAST(d.salary AS NVARCHAR(50)),
        CAST(i.salary AS NVARCHAR(50)),
        'Salary adjustment'
    FROM inserted i
    INNER JOIN deleted d ON i.employee_id = d.employee_id
    WHERE i.salary != d.salary;

    -- Capture status changes
    INSERT INTO employee_change_history (employee_id, field_name, old_value, new_value, change_reason)
    SELECT
        i.employee_id,
        'status',
        d.status,
        i.status,
        CASE
            WHEN i.status = 'Terminated' THEN 'Employment ended'
            WHEN i.status = 'Leave' THEN 'Leave of absence'
            WHEN i.status = 'Active' THEN 'Returned to active status'
            ELSE 'Status change'
        END
    FROM inserted i
    INNER JOIN deleted d ON i.employee_id = d.employee_id
    WHERE i.status != d.status;
END;
```

**Key Features**:
- Automatic audit trail for compliance
- Captures who made changes and when
- Can be extended to track any field changes

### Pattern 3: Employee Substitute Availability

**Use Case**: Find available substitutes for a specific date and subject area.

```sql
DECLARE @RequiredDate DATE = '2025-10-25';
DECLARE @SubjectArea NVARCHAR(50) = 'Mathematics';
DECLARE @SchoolSite NVARCHAR(100) = 'Central High School';

WITH SubstituteAvailability AS (
    SELECT
        s.substitute_id,
        s.first_name + ' ' + s.last_name AS substitute_name,
        s.phone,
        s.email,
        sc.credential_type,
        sc.subject_area,
        sc.expiration_date,
        -- Check if already booked for this date
        CASE
            WHEN EXISTS (
                SELECT 1
                FROM substitute_assignments sa
                WHERE sa.substitute_id = s.substitutes_id
                  AND sa.assignment_date = @RequiredDate
            ) THEN 0
            ELSE 1
        END AS is_available,
        -- Preference score (higher is better)
        (CASE WHEN s.preferred_schools LIKE '%' + @SchoolSite + '%' THEN 10 ELSE 0 END) +
        (CASE WHEN s.years_experience > 5 THEN 5 ELSE s.years_experience END) AS preference_score
    FROM substitutes s
    INNER JOIN substitute_credentials sc ON s.substitute_id = sc.substitute_id
    WHERE s.status = 'Active'
      AND sc.subject_area = @SubjectArea
      AND sc.expiration_date > GETDATE()
      AND s.availability_status = 'Available'
)
SELECT
    substitute_id,
    substitute_name,
    phone,
    email,
    credential_type,
    expiration_date,
    preference_score
FROM SubstituteAvailability
WHERE is_available = 1
ORDER BY preference_score DESC, substitute_name;
```

**Key Features**:
- Checks credential validity and expiration
- Verifies substitute is not already booked
- Ranks substitutes by preference and experience
- Subject area matching for qualified coverage

---

## Credential Tracking and Verification

### Pattern 4: Expiring Credentials Alert

**Use Case**: Identify credentials expiring within the next 90 days that need renewal.

```sql
DECLARE @WarningDays INT = 90;

WITH ExpiringCredentials AS (
    SELECT
        e.employee_id,
        e.first_name + ' ' + e.last_name AS employee_name,
        e.email,
        c.credential_type,
        c.credential_number,
        c.issue_date,
        c.expiration_date,
        DATEDIFF(DAY, GETDATE(), c.expiration_date) AS days_until_expiration,
        CASE
            WHEN DATEDIFF(DAY, GETDATE(), c.expiration_date) <= 30 THEN 'Critical'
            WHEN DATEDIFF(DAY, GETDATE(), c.expiration_date) <= 60 THEN 'High'
            WHEN DATEDIFF(DAY, GETDATE(), c.expiration_date) <= 90 THEN 'Medium'
            ELSE 'Low'
        END AS urgency_level,
        -- Check if renewal is in progress
        CASE
            WHEN EXISTS (
                SELECT 1
                FROM credential_renewals cr
                WHERE cr.credential_id = c.credential_id
                  AND cr.renewal_status IN ('Pending', 'In Progress')
            ) THEN 'Yes'
            ELSE 'No'
        END AS renewal_in_progress
    FROM employees e
    INNER JOIN credentials c ON e.employee_id = c.employee_id
    WHERE e.status = 'Active'
      AND c.expiration_date IS NOT NULL
      AND c.expiration_date BETWEEN GETDATE() AND DATEADD(DAY, @WarningDays, GETDATE())
)
SELECT
    employee_id,
    employee_name,
    email,
    credential_type,
    credential_number,
    issue_date,
    expiration_date,
    days_until_expiration,
    urgency_level,
    renewal_in_progress
FROM ExpiringCredentials
ORDER BY days_until_expiration ASC, urgency_level DESC;
```

**Key Features**:
- Tiered urgency levels for prioritization
- Checks if renewal is already in progress
- Configurable warning window
- Email-ready output for notifications

### Pattern 5: Credential Subject Area Crosswalk

**Use Case**: Map legacy credential codes to new system codes for data migration or integration.

```sql
-- Crosswalk table structure
CREATE TABLE credential_subject_crosswalk (
    crosswalk_id INT IDENTITY(1,1) PRIMARY KEY,
    legacy_code NVARCHAR(50) NOT NULL,
    legacy_description NVARCHAR(200),
    new_system_code NVARCHAR(50) NOT NULL,
    new_system_description NVARCHAR(200),
    subject_area NVARCHAR(100),
    grade_level_min INT,
    grade_level_max INT,
    effective_date DATE DEFAULT GETDATE(),
    notes NVARCHAR(500),
    CONSTRAINT UQ_legacy_code UNIQUE (legacy_code)
);

-- Query to validate legacy credentials against crosswalk
WITH LegacyCredentialValidation AS (
    SELECT
        lc.employee_id,
        lc.legacy_credential_code,
        lc.legacy_description,
        csc.new_system_code,
        csc.new_system_description,
        csc.subject_area,
        CASE
            WHEN csc.crosswalk_id IS NULL THEN 'Unmapped - Manual Review Required'
            WHEN csc.new_system_code IS NULL THEN 'No Equivalent in New System'
            ELSE 'Mapped'
        END AS mapping_status,
        csc.notes
    FROM legacy_credentials lc
    LEFT JOIN credential_subject_crosswalk csc ON lc.legacy_credential_code = csc.legacy_code
)
SELECT
    employee_id,
    legacy_credential_code,
    legacy_description,
    new_system_code,
    new_system_description,
    subject_area,
    mapping_status,
    notes
FROM LegacyCredentialValidation
WHERE mapping_status != 'Mapped'
ORDER BY mapping_status, employee_id;
```

**Key Features**:
- Handles one-to-one and one-to-many credential mappings
- Identifies unmapped credentials for manual review
- Supports grade level restrictions
- Useful for system migrations and data integration

### Pattern 6: Credential Compliance by Department

**Use Case**: Verify that all employees in a department have required credentials for their positions.

```sql
WITH DepartmentCredentialRequirements AS (
    SELECT
        d.department_id,
        d.department_name,
        jr.job_title,
        jr.required_credential_type,
        jr.is_mandatory
    FROM departments d
    INNER JOIN job_requirements jr ON d.department_id = jr.department_id
    WHERE jr.is_mandatory = 1
),
EmployeeCredentialStatus AS (
    SELECT
        e.employee_id,
        e.first_name + ' ' + e.last_name AS employee_name,
        e.job_title,
        e.department_id,
        dcr.required_credential_type,
        -- Check if employee has valid credential
        CASE
            WHEN EXISTS (
                SELECT 1
                FROM credentials c
                WHERE c.employee_id = e.employee_id
                  AND c.credential_type = dcr.required_credential_type
                  AND (c.expiration_date IS NULL OR c.expiration_date > GETDATE())
            ) THEN 'Compliant'
            ELSE 'Non-Compliant'
        END AS compliance_status,
        -- Get expiration date if credential exists
        (SELECT TOP 1 c.expiration_date
         FROM credentials c
         WHERE c.employee_id = e.employee_id
           AND c.credential_type = dcr.required_credential_type
         ORDER BY c.expiration_date DESC) AS credential_expiration
    FROM employees e
    INNER JOIN DepartmentCredentialRequirements dcr ON e.department_id = dcr.department_id
    WHERE e.status = 'Active'
)
SELECT
    department_id,
    employee_id,
    employee_name,
    job_title,
    required_credential_type,
    compliance_status,
    credential_expiration,
    CASE
        WHEN compliance_status = 'Non-Compliant' THEN 'Immediate Action Required'
        WHEN credential_expiration <= DATEADD(DAY, 90, GETDATE()) THEN 'Renewal Needed Soon'
        ELSE 'OK'
    END AS action_required
FROM EmployeeCredentialStatus
WHERE compliance_status = 'Non-Compliant'
   OR credential_expiration <= DATEADD(DAY, 90, GETDATE())
ORDER BY compliance_status DESC, credential_expiration ASC;
```

**Key Features**:
- Enforces mandatory credential requirements
- Identifies non-compliant employees
- Proactive renewal warnings
- Department-specific compliance tracking

---

## Department and Organization Patterns

### Pattern 7: Department Budget Allocation with Rollup

**Use Case**: Calculate department budgets with hierarchical rollup to school/district level.

```sql
WITH RECURSIVE DepartmentHierarchy AS (
    -- Anchor: Top-level departments (no parent)
    SELECT
        department_id,
        parent_department_id,
        department_name,
        department_type,
        budget_allocated,
        1 AS hierarchy_level,
        CAST(department_name AS NVARCHAR(1000)) AS hierarchy_path
    FROM departments
    WHERE parent_department_id IS NULL

    UNION ALL

    -- Recursive: Child departments
    SELECT
        d.department_id,
        d.parent_department_id,
        d.department_name,
        d.department_type,
        d.budget_allocated,
        dh.hierarchy_level + 1,
        CAST(dh.hierarchy_path + ' > ' + d.department_name AS NVARCHAR(1000))
    FROM departments d
    INNER JOIN DepartmentHierarchy dh ON d.parent_department_id = dh.department_id
    WHERE dh.hierarchy_level < 10
),
BudgetRollup AS (
    SELECT
        dh.department_id,
        dh.department_name,
        dh.department_type,
        dh.hierarchy_level,
        dh.hierarchy_path,
        dh.budget_allocated AS direct_budget,
        -- Sum of all child department budgets
        (SELECT SUM(child.budget_allocated)
         FROM DepartmentHierarchy child
         WHERE child.hierarchy_path LIKE dh.hierarchy_path + '%'
           AND child.department_id != dh.department_id) AS child_budgets_total,
        -- Total budget including children
        dh.budget_allocated +
        ISNULL((SELECT SUM(child.budget_allocated)
                FROM DepartmentHierarchy child
                WHERE child.hierarchy_path LIKE dh.hierarchy_path + '%'
                  AND child.department_id != dh.department_id), 0) AS total_budget_with_children
    FROM DepartmentHierarchy dh
)
SELECT
    department_id,
    REPLICATE('  ', hierarchy_level - 1) + department_name AS department_name_indented,
    department_type,
    hierarchy_level,
    hierarchy_path,
    direct_budget,
    child_budgets_total,
    total_budget_with_children,
    CAST(ROUND((direct_budget * 100.0 / NULLIF(total_budget_with_children, 0)), 2) AS DECIMAL(5,2)) AS pct_of_total
FROM BudgetRollup
ORDER BY hierarchy_path;
```

**Key Features**:
- Recursive hierarchy navigation
- Budget rollup from child to parent departments
- Percentage calculation for budget distribution
- Visual indentation for hierarchy display

### Pattern 8: Cross-Department Resource Sharing

**Use Case**: Track employees who work across multiple departments or school sites.

```sql
WITH EmployeeMultipleAssignments AS (
    SELECT
        e.employee_id,
        e.first_name + ' ' + e.last_name AS employee_name,
        e.primary_department_id,
        COUNT(DISTINCT ea.department_id) AS department_count,
        COUNT(DISTINCT d.school_site) AS school_site_count,
        STRING_AGG(d.department_name, ', ') WITHIN GROUP (ORDER BY ea.fte_percentage DESC) AS departments,
        SUM(ea.fte_percentage) AS total_fte
    FROM employees e
    INNER JOIN employee_assignments ea ON e.employee_id = ea.employee_id
    INNER JOIN departments d ON ea.department_id = d.department_id
    WHERE ea.assignment_end_date IS NULL OR ea.assignment_end_date > GETDATE()
    GROUP BY e.employee_id, e.first_name, e.last_name, e.primary_department_id
    HAVING COUNT(DISTINCT ea.department_id) > 1
)
SELECT
    employee_id,
    employee_name,
    department_count,
    school_site_count,
    departments,
    total_fte,
    CASE
        WHEN total_fte > 1.0 THEN 'Over-allocated (' + CAST(total_fte AS NVARCHAR(10)) + ')'
        WHEN total_fte < 1.0 THEN 'Under-allocated (' + CAST(total_fte AS NVARCHAR(10)) + ')'
        ELSE 'Fully allocated'
    END AS allocation_status
FROM EmployeeMultipleAssignments
ORDER BY department_count DESC, school_site_count DESC;
```

**Key Features**:
- Identifies shared resources across departments
- Calculates total FTE allocation
- Detects over/under-allocation issues
- Uses STRING_AGG for department list aggregation

---

## Student Enrollment Patterns

### Pattern 9: Student Course Enrollment with Prerequisites

**Use Case**: Verify students meet prerequisites before enrolling in advanced courses.

```sql
CREATE FUNCTION dbo.fn_check_prerequisites (
    @student_id INT,
    @course_id INT
)
RETURNS TABLE
AS
RETURN
(
    WITH CoursePrerequisites AS (
        SELECT
            cp.prerequisite_course_id,
            c.course_code,
            c.course_name,
            cp.minimum_grade_required
        FROM course_prerequisites cp
        INNER JOIN courses c ON cp.prerequisite_course_id = c.course_id
        WHERE cp.course_id = @course_id
    ),
    StudentCompletedCourses AS (
        SELECT
            sc.course_id,
            sc.final_grade,
            sc.completion_date
        FROM student_courses sc
        WHERE sc.student_id = @student_id
          AND sc.completion_status = 'Completed'
    )
    SELECT
        cp.prerequisite_course_id,
        cp.course_code,
        cp.course_name,
        cp.minimum_grade_required,
        scc.final_grade AS student_grade,
        CASE
            WHEN scc.course_id IS NULL THEN 'Not Taken'
            WHEN scc.final_grade >= cp.minimum_grade_required THEN 'Met'
            ELSE 'Not Met - Grade Too Low'
        END AS prerequisite_status
    FROM CoursePrerequisites cp
    LEFT JOIN StudentCompletedCourses scc ON cp.prerequisite_course_id = scc.course_id
);

-- Usage example
DECLARE @student_id INT = 12345;
DECLARE @course_id INT = 789;

SELECT
    c.course_code,
    c.course_name,
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM dbo.fn_check_prerequisites(@student_id, @course_id)
            WHERE prerequisite_status != 'Met'
        ) THEN 'Not Eligible - Missing Prerequisites'
        ELSE 'Eligible'
    END AS enrollment_eligibility,
    -- List unmet prerequisites
    (SELECT STRING_AGG(course_name + ' (' + prerequisite_status + ')', '; ')
     FROM dbo.fn_check_prerequisites(@student_id, @course_id)
     WHERE prerequisite_status != 'Met') AS unmet_prerequisites
FROM courses c
WHERE c.course_id = @course_id;
```

**Key Features**:
- Table-valued function for reusability
- Checks multiple prerequisites
- Validates minimum grade requirements
- Clear eligibility determination

### Pattern 10: Student Enrollment Capacity Management

**Use Case**: Track course section capacity and available seats for enrollment.

```sql
WITH SectionCapacity AS (
    SELECT
        cs.section_id,
        c.course_code,
        c.course_name,
        cs.section_number,
        cs.max_capacity,
        cs.waitlist_capacity,
        t.first_name + ' ' + t.last_name AS instructor_name,
        cs.meeting_days,
        cs.meeting_time,
        cs.room_number,
        -- Count current enrollments
        COUNT(DISTINCT se.student_id) AS current_enrollment,
        -- Count waitlist
        (SELECT COUNT(*)
         FROM section_waitlist sw
         WHERE sw.section_id = cs.section_id
           AND sw.waitlist_status = 'Active') AS waitlist_count,
        -- Calculate available seats
        cs.max_capacity - COUNT(DISTINCT se.student_id) AS seats_available,
        cs.waitlist_capacity - (SELECT COUNT(*)
                                FROM section_waitlist sw
                                WHERE sw.section_id = cs.section_id
                                  AND sw.waitlist_status = 'Active') AS waitlist_seats_available
    FROM course_sections cs
    INNER JOIN courses c ON cs.course_id = c.course_id
    LEFT JOIN teachers t ON cs.instructor_id = t.teacher_id
    LEFT JOIN student_enrollments se ON cs.section_id = se.section_id
                                     AND se.enrollment_status = 'Active'
    WHERE cs.academic_term = '2025 Fall'
      AND cs.section_status = 'Open'
    GROUP BY cs.section_id, c.course_code, c.course_name, cs.section_number,
             cs.max_capacity, cs.waitlist_capacity, t.first_name, t.last_name,
             cs.meeting_days, cs.meeting_time, cs.room_number
)
SELECT
    section_id,
    course_code,
    course_name,
    section_number,
    instructor_name,
    meeting_days,
    meeting_time,
    room_number,
    max_capacity,
    current_enrollment,
    seats_available,
    waitlist_count,
    waitlist_seats_available,
    CAST(ROUND((current_enrollment * 100.0 / max_capacity), 1) AS DECIMAL(5,1)) AS pct_full,
    CASE
        WHEN seats_available > 10 THEN 'Open'
        WHEN seats_available > 0 THEN 'Nearly Full'
        WHEN waitlist_seats_available > 0 THEN 'Full - Waitlist Available'
        ELSE 'Full - Waitlist Full'
    END AS enrollment_status
FROM SectionCapacity
ORDER BY course_code, section_number;
```

**Key Features**:
- Real-time capacity tracking
- Waitlist management
- Percentage full calculation
- Status indicators for enrollment decisions

---

## Course and Schedule Management

### Pattern 11: Teacher Schedule Conflict Detection

**Use Case**: Identify scheduling conflicts where a teacher is assigned to multiple classes at the same time.

```sql
WITH TeacherSchedule AS (
    SELECT
        t.teacher_id,
        t.first_name + ' ' + t.last_name AS teacher_name,
        cs.section_id,
        c.course_code,
        c.course_name,
        cs.section_number,
        cs.meeting_days,
        cs.start_time,
        cs.end_time,
        cs.room_number,
        cs.academic_term
    FROM teachers t
    INNER JOIN course_sections cs ON t.teacher_id = cs.instructor_id
    INNER JOIN courses c ON cs.course_id = c.course_id
    WHERE cs.section_status = 'Active'
      AND cs.academic_term = '2025 Fall'
),
ScheduleConflicts AS (
    SELECT
        ts1.teacher_id,
        ts1.teacher_name,
        ts1.section_id AS section_id_1,
        ts1.course_code + '-' + CAST(ts1.section_number AS NVARCHAR(10)) AS section_1,
        ts1.meeting_days AS days_1,
        CAST(ts1.start_time AS TIME) AS start_time_1,
        CAST(ts1.end_time AS TIME) AS end_time_1,
        ts1.room_number AS room_1,
        ts2.section_id AS section_id_2,
        ts2.course_code + '-' + CAST(ts2.section_number AS NVARCHAR(10)) AS section_2,
        ts2.meeting_days AS days_2,
        CAST(ts2.start_time AS TIME) AS start_time_2,
        CAST(ts2.end_time AS TIME) AS end_time_2,
        ts2.room_number AS room_2
    FROM TeacherSchedule ts1
    INNER JOIN TeacherSchedule ts2 ON ts1.teacher_id = ts2.teacher_id
                                    AND ts1.section_id < ts2.section_id -- Avoid duplicates
    WHERE ts1.academic_term = ts2.academic_term
      -- Check if days overlap
      AND (ts1.meeting_days LIKE '%M%' AND ts2.meeting_days LIKE '%M%'
        OR ts1.meeting_days LIKE '%T%' AND ts2.meeting_days LIKE '%T%'
        OR ts1.meeting_days LIKE '%W%' AND ts2.meeting_days LIKE '%W%'
        OR ts1.meeting_days LIKE '%R%' AND ts2.meeting_days LIKE '%R%'
        OR ts1.meeting_days LIKE '%F%' AND ts2.meeting_days LIKE '%F%')
      -- Check if times overlap
      AND (
        (ts1.start_time <= ts2.start_time AND ts1.end_time > ts2.start_time)
        OR (ts2.start_time <= ts1.start_time AND ts2.end_time > ts1.start_time)
      )
)
SELECT
    teacher_id,
    teacher_name,
    section_1,
    days_1,
    start_time_1,
    end_time_1,
    room_1,
    section_2,
    days_2,
    start_time_2,
    end_time_2,
    room_2,
    'CONFLICT' AS status
FROM ScheduleConflicts
ORDER BY teacher_name, start_time_1;
```

**Key Features**:
- Detects overlapping time slots
- Checks day-of-week conflicts
- Handles multiple section assignments
- Self-join pattern for conflict detection

### Pattern 12: Room Utilization Analysis

**Use Case**: Analyze classroom usage to optimize room assignments and identify underutilized spaces.

```sql
WITH RoomSchedule AS (
    SELECT
        r.room_id,
        r.room_number,
        r.building_name,
        r.room_capacity,
        r.room_type,
        cs.section_id,
        cs.meeting_days,
        cs.start_time,
        cs.end_time,
        se.current_enrollment,
        -- Calculate duration in hours
        DATEDIFF(MINUTE, cs.start_time, cs.end_time) / 60.0 AS class_duration_hours
    FROM rooms r
    LEFT JOIN course_sections cs ON r.room_id = cs.room_id
                                 AND cs.section_status = 'Active'
                                 AND cs.academic_term = '2025 Fall'
    LEFT JOIN (
        SELECT section_id, COUNT(*) AS current_enrollment
        FROM student_enrollments
        WHERE enrollment_status = 'Active'
        GROUP BY section_id
    ) se ON cs.section_id = se.section_id
),
RoomUtilization AS (
    SELECT
        room_id,
        room_number,
        building_name,
        room_capacity,
        room_type,
        -- Count unique sections
        COUNT(DISTINCT section_id) AS sections_count,
        -- Calculate total hours used per week
        SUM(
            class_duration_hours *
            (LEN(meeting_days) - LEN(REPLACE(meeting_days, 'M', '')) +
             LEN(meeting_days) - LEN(REPLACE(meeting_days, 'T', '')) +
             LEN(meeting_days) - LEN(REPLACE(meeting_days, 'W', '')) +
             LEN(meeting_days) - LEN(REPLACE(meeting_days, 'R', '')) +
             LEN(meeting_days) - LEN(REPLACE(meeting_days, 'F', '')))
        ) AS weekly_hours_used,
        -- Average capacity utilization
        AVG(CAST(current_enrollment AS FLOAT) / NULLIF(room_capacity, 0)) * 100 AS avg_capacity_utilization_pct
    FROM RoomSchedule
    GROUP BY room_id, room_number, building_name, room_capacity, room_type
)
SELECT
    room_number,
    building_name,
    room_type,
    room_capacity,
    sections_count,
    ROUND(ISNULL(weekly_hours_used, 0), 1) AS weekly_hours_used,
    ROUND(ISNULL(weekly_hours_used, 0) / 40.0 * 100, 1) AS utilization_pct, -- Assuming 40-hour week
    ROUND(ISNULL(avg_capacity_utilization_pct, 0), 1) AS avg_capacity_pct,
    CASE
        WHEN weekly_hours_used >= 35 THEN 'High Utilization'
        WHEN weekly_hours_used >= 20 THEN 'Moderate Utilization'
        WHEN weekly_hours_used > 0 THEN 'Low Utilization'
        ELSE 'Not Used'
    END AS utilization_status
FROM RoomUtilization
ORDER BY utilization_pct DESC;
```

**Key Features**:
- Calculates weekly hours of room usage
- Tracks capacity utilization (students vs room size)
- Identifies underutilized spaces
- Supports space planning decisions

---

## Leave and Absence Tracking

### Pattern 13: Employee Leave Balance and Accrual

**Use Case**: Calculate current leave balances with accrual tracking and usage history.

```sql
WITH LeaveAccrual AS (
    SELECT
        e.employee_id,
        lt.leave_type,
        lt.accrual_rate_per_pay_period,
        lt.max_accrual_limit,
        -- Calculate total accrued since hire date
        DATEDIFF(MONTH, e.hire_date, GETDATE()) * lt.accrual_rate_per_pay_period AS total_accrued,
        -- Sum of used leave
        ISNULL(SUM(lu.hours_used), 0) AS total_used,
        -- Current balance
        (DATEDIFF(MONTH, e.hire_date, GETDATE()) * lt.accrual_rate_per_pay_period) -
        ISNULL(SUM(lu.hours_used), 0) AS current_balance,
        -- Check if at max limit
        CASE
            WHEN (DATEDIFF(MONTH, e.hire_date, GETDATE()) * lt.accrual_rate_per_pay_period) -
                 ISNULL(SUM(lu.hours_used), 0) >= lt.max_accrual_limit
            THEN 1
            ELSE 0
        END AS is_at_max
    FROM employees e
    CROSS JOIN leave_types lt
    LEFT JOIN leave_usage lu ON e.employee_id = lu.employee_id
                              AND lt.leave_type_id = lu.leave_type_id
    WHERE e.status = 'Active'
    GROUP BY e.employee_id, lt.leave_type, lt.leave_type_id,
             lt.accrual_rate_per_pay_period, lt.max_accrual_limit, e.hire_date
)
SELECT
    e.employee_id,
    e.first_name + ' ' + e.last_name AS employee_name,
    la.leave_type,
    la.total_accrued,
    la.total_used,
    CASE
        WHEN la.current_balance > la.max_accrual_limit THEN la.max_accrual_limit
        ELSE la.current_balance
    END AS current_balance,
    la.max_accrual_limit,
    la.is_at_max,
    CASE
        WHEN la.is_at_max = 1 THEN 'Warning: Use leave to avoid losing accrual'
        WHEN la.current_balance >= la.max_accrual_limit * 0.9 THEN 'Approaching max limit'
        ELSE 'Normal'
    END AS status_message
FROM employees e
INNER JOIN LeaveAccrual la ON e.employee_id = la.employee_id
WHERE e.status = 'Active'
ORDER BY e.last_name, la.leave_type;
```

**Key Features**:
- Automatic accrual calculation based on tenure
- Enforces maximum accrual limits
- Identifies employees at risk of losing leave
- Tracks multiple leave types per employee

### Pattern 14: Substitute Coverage Gap Detection

**Use Case**: Identify approved leave dates without confirmed substitute coverage.

```sql
WITH ApprovedLeave AS (
    SELECT
        lr.leave_request_id,
        lr.employee_id,
        e.first_name + ' ' + e.last_name AS employee_name,
        lr.leave_start_date,
        lr.leave_end_date,
        lr.leave_type,
        lr.approval_status,
        d.department_name,
        d.school_site,
        -- Generate all dates in leave period
        DATEADD(DAY, n.number, lr.leave_start_date) AS leave_date
    FROM leave_requests lr
    INNER JOIN employees e ON lr.employee_id = e.employee_id
    INNER JOIN departments d ON e.department_id = d.department_id
    CROSS JOIN master..spt_values n
    WHERE lr.approval_status = 'Approved'
      AND n.type = 'P'
      AND DATEADD(DAY, n.number, lr.leave_start_date) <= lr.leave_end_date
      AND lr.leave_start_date >= GETDATE()
),
SubstituteCoverage AS (
    SELECT
        sa.original_employee_id,
        sa.assignment_date,
        sa.substitute_id,
        s.first_name + ' ' + s.last_name AS substitute_name,
        sa.confirmation_status
    FROM substitute_assignments sa
    INNER JOIN substitutes s ON sa.substitute_id = s.substitute_id
    WHERE sa.assignment_date >= GETDATE()
)
SELECT
    al.employee_id,
    al.employee_name,
    al.department_name,
    al.school_site,
    al.leave_date,
    al.leave_type,
    ISNULL(sc.substitute_name, 'NO COVERAGE') AS substitute_assigned,
    ISNULL(sc.confirmation_status, 'UNASSIGNED') AS coverage_status,
    DATEDIFF(DAY, GETDATE(), al.leave_date) AS days_until_leave,
    CASE
        WHEN sc.substitute_id IS NULL THEN 'CRITICAL - No Substitute Assigned'
        WHEN sc.confirmation_status = 'Tentative' THEN 'WARNING - Not Confirmed'
        WHEN sc.confirmation_status = 'Confirmed' THEN 'OK'
        ELSE 'UNKNOWN'
    END AS alert_level
FROM ApprovedLeave al
LEFT JOIN SubstituteCoverage sc ON al.employee_id = sc.original_employee_id
                                 AND al.leave_date = sc.assignment_date
WHERE sc.substitute_id IS NULL -- No substitute assigned
   OR sc.confirmation_status != 'Confirmed' -- Not confirmed
ORDER BY days_until_leave, al.school_site, al.employee_name;
```

**Key Features**:
- Generates all dates in leave period
- Checks substitute assignment status
- Prioritizes by urgency (days until leave)
- Identifies gaps in coverage planning

---

## Payroll and Compensation Patterns

### Pattern 15: Salary Step and Column Progression

**Use Case**: Calculate salary adjustments based on step/column progression in collective bargaining agreements.

```sql
CREATE TABLE salary_schedule (
    schedule_id INT IDENTITY(1,1) PRIMARY KEY,
    position_type NVARCHAR(100),
    step_number INT,
    column_letter CHAR(1),
    annual_salary DECIMAL(10,2),
    hourly_rate DECIMAL(8,2),
    effective_date DATE
);

-- Calculate next salary progression
WITH EmployeeCurrentSalary AS (
    SELECT
        e.employee_id,
        e.first_name + ' ' + e.last_name AS employee_name,
        e.position_type,
        e.current_step,
        e.current_column,
        e.hire_date,
        DATEDIFF(YEAR, e.hire_date, GETDATE()) AS years_of_service,
        ss_current.annual_salary AS current_annual_salary,
        ss_current.hourly_rate AS current_hourly_rate
    FROM employees e
    INNER JOIN salary_schedule ss_current ON e.position_type = ss_current.position_type
                                          AND e.current_step = ss_current.step_number
                                          AND e.current_column = ss_current.column_letter
    WHERE e.status = 'Active'
),
SalaryProgression AS (
    SELECT
        ecs.employee_id,
        ecs.employee_name,
        ecs.position_type,
        ecs.current_step,
        ecs.current_column,
        ecs.current_annual_salary,
        ecs.years_of_service,
        -- Next step (vertical progression)
        ss_next_step.step_number AS next_step,
        ss_next_step.column_letter AS next_step_column,
        ss_next_step.annual_salary AS next_step_salary,
        ss_next_step.annual_salary - ecs.current_annual_salary AS step_increase_amount,
        -- Next column (horizontal progression - education/credential)
        ss_next_col.step_number AS next_col_step,
        ss_next_col.column_letter AS next_column,
        ss_next_col.annual_salary AS next_column_salary,
        ss_next_col.annual_salary - ecs.current_annual_salary AS column_increase_amount
    FROM EmployeeCurrentSalary ecs
    LEFT JOIN salary_schedule ss_next_step ON ecs.position_type = ss_next_step.position_type
                                            AND ecs.current_step + 1 = ss_next_step.step_number
                                            AND ecs.current_column = ss_next_step.column_letter
    LEFT JOIN salary_schedule ss_next_col ON ecs.position_type = ss_next_col.position_type
                                           AND ecs.current_step = ss_next_col.step_number
                                           AND ASCII(ecs.current_column) + 1 = ASCII(ss_next_col.column_letter)
)
SELECT
    employee_id,
    employee_name,
    position_type,
    CAST(current_step AS NVARCHAR(5)) + current_column AS current_placement,
    FORMAT(current_annual_salary, 'C', 'en-US') AS current_salary,
    years_of_service,
    CASE
        WHEN next_step IS NOT NULL THEN
            CAST(next_step AS NVARCHAR(5)) + next_step_column + ' (' +
            FORMAT(next_step_salary, 'C', 'en-US') + ', +' +
            FORMAT(step_increase_amount, 'C', 'en-US') + ')'
        ELSE 'At Max Step'
    END AS next_step_progression,
    CASE
        WHEN next_column IS NOT NULL THEN
            CAST(next_col_step AS NVARCHAR(5)) + next_column + ' (' +
            FORMAT(next_column_salary, 'C', 'en-US') + ', +' +
            FORMAT(column_increase_amount, 'C', 'en-US') + ')'
        ELSE 'At Max Column'
    END AS next_column_progression
FROM SalaryProgression
ORDER BY position_type, current_step, current_column;
```

**Key Features**:
- Handles both step (years of service) and column (education) progression
- Calculates increase amounts for budgeting
- Identifies employees at maximum salary
- Supports collective bargaining agreement structures

---

## Reporting and Analytics Patterns

### Pattern 16: Employee Demographics Dashboard

**Use Case**: Generate demographic summary for diversity reporting and analysis.

```sql
WITH EmployeeDemographics AS (
    SELECT
        e.employee_id,
        e.gender,
        e.ethnicity,
        e.birth_date,
        DATEDIFF(YEAR, e.birth_date, GETDATE()) AS age,
        CASE
            WHEN DATEDIFF(YEAR, e.birth_date, GETDATE()) < 30 THEN '< 30'
            WHEN DATEDIFF(YEAR, e.birth_date, GETDATE()) < 40 THEN '30-39'
            WHEN DATEDIFF(YEAR, e.birth_date, GETDATE()) < 50 THEN '40-49'
            WHEN DATEDIFF(YEAR, e.birth_date, GETDATE()) < 60 THEN '50-59'
            ELSE '60+'
        END AS age_group,
        d.department_name,
        d.school_site,
        e.job_title,
        e.employment_type,
        DATEDIFF(YEAR, e.hire_date, GETDATE()) AS years_of_service
    FROM employees e
    INNER JOIN departments d ON e.department_id = d.department_id
    WHERE e.status = 'Active'
)
SELECT
    'Gender Distribution' AS metric_category,
    gender AS metric_value,
    COUNT(*) AS employee_count,
    CAST(ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS DECIMAL(5,2)) AS percentage
FROM EmployeeDemographics
GROUP BY gender

UNION ALL

SELECT
    'Ethnicity Distribution' AS metric_category,
    ethnicity AS metric_value,
    COUNT(*) AS employee_count,
    CAST(ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS DECIMAL(5,2)) AS percentage
FROM EmployeeDemographics
GROUP BY ethnicity

UNION ALL

SELECT
    'Age Group Distribution' AS metric_category,
    age_group AS metric_value,
    COUNT(*) AS employee_count,
    CAST(ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS DECIMAL(5,2)) AS percentage
FROM EmployeeDemographics
GROUP BY age_group

UNION ALL

SELECT
    'Employment Type' AS metric_category,
    employment_type AS metric_value,
    COUNT(*) AS employee_count,
    CAST(ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS DECIMAL(5,2)) AS percentage
FROM EmployeeDemographics
GROUP BY employment_type

ORDER BY metric_category, employee_count DESC;
```

**Key Features**:
- Multiple demographic dimensions in single query
- Percentage calculations for reporting
- Age grouping for privacy compliance
- UNION ALL for consolidated dashboard output

### Pattern 17: Year-over-Year Trend Analysis

**Use Case**: Compare current year metrics against prior years for trend identification.

```sql
WITH YearlyMetrics AS (
    SELECT
        YEAR(hire_date) AS hire_year,
        COUNT(*) AS new_hires,
        AVG(salary) AS avg_starting_salary
    FROM employees
    GROUP BY YEAR(hire_date)
),
TurnoverMetrics AS (
    SELECT
        YEAR(termination_date) AS termination_year,
        COUNT(*) AS terminations
    FROM employees
    WHERE termination_date IS NOT NULL
    GROUP BY YEAR(termination_date)
),
HeadcountMetrics AS (
    SELECT
        year_number,
        (SELECT COUNT(*)
         FROM employees
         WHERE hire_date <= DATEFROMPARTS(year_number, 12, 31)
           AND (termination_date IS NULL OR termination_date > DATEFROMPARTS(year_number, 12, 31))
        ) AS eoy_headcount
    FROM (VALUES (2021), (2022), (2023), (2024), (2025)) AS Years(year_number)
)
SELECT
    hm.year_number AS fiscal_year,
    hm.eoy_headcount,
    LAG(hm.eoy_headcount) OVER (ORDER BY hm.year_number) AS prior_year_headcount,
    hm.eoy_headcount - LAG(hm.eoy_headcount) OVER (ORDER BY hm.year_number) AS headcount_change,
    ym.new_hires,
    tm.terminations,
    CAST(ROUND((tm.terminations * 100.0 / NULLIF(hm.eoy_headcount, 0)), 2) AS DECIMAL(5,2)) AS turnover_rate,
    FORMAT(ym.avg_starting_salary, 'C', 'en-US') AS avg_starting_salary,
    FORMAT(ym.avg_starting_salary - LAG(ym.avg_starting_salary) OVER (ORDER BY hm.year_number), 'C', 'en-US') AS salary_yoy_change
FROM HeadcountMetrics hm
LEFT JOIN YearlyMetrics ym ON hm.year_number = ym.hire_year
LEFT JOIN TurnoverMetrics tm ON hm.year_number = tm.termination_year
ORDER BY hm.year_number;
```

**Key Features**:
- Uses LAG window function for year-over-year comparison
- Calculates turnover rate
- Tracks headcount changes
- Supports multi-year trend analysis

---

## Best Practices Summary

1. **Use CTEs for readability** - Break complex queries into logical steps
2. **Window functions for rankings and running totals** - More efficient than subqueries
3. **NULL-safe date comparisons** - Always handle open-ended date ranges properly
4. **String aggregation for lists** - Use STRING_AGG (SQL Server 2017+) or XML PATH for older versions
5. **Recursive CTEs for hierarchies** - Essential for organizational charts and reporting structures
6. **Table-valued functions for reusability** - Encapsulate complex logic for multiple uses
7. **Index supporting columns** - Include frequently filtered/joined columns in indexes
8. **Parameterize for flexibility** - Use variables for dates, thresholds, and filters
9. **Document business rules** - Add comments explaining credential requirements, accrual rules, etc.
10. **Test with realistic data volumes** - Educational HR databases can be large; ensure queries scale

---

## Additional Resources

For more advanced SQL techniques, see:
- `advanced_techniques.md` - 15 advanced SQL concepts with code examples
- `query_optimization.md` - Execution plan analysis and performance tuning
- `sql_antipatterns.md` - Common mistakes to avoid in HR/education queries

<?php
require_once 'includes/config.php';

if (!isset($_SESSION['student_id'])) {
    header('Location: index.php');
    exit();
}

$student_id = $_SESSION['student_id'];
$query = "SELECT * FROM students WHERE id = $student_id";
$result = mysqli_query($conn, $query);
$student = mysqli_fetch_assoc($result);

$entry_count_query = "SELECT COUNT(*) as total FROM logbook_entries WHERE student_id = $student_id";
$entry_count = mysqli_fetch_assoc(mysqli_query($conn, $entry_count_query));

$submitted_query = "SELECT COUNT(*) as total FROM logbook_entries WHERE student_id = $student_id AND status = 'submitted'";
$submitted = mysqli_fetch_assoc(mysqli_query($conn, $submitted_query));

$assessment_query = "SELECT COUNT(*) as total FROM assessments WHERE student_id = $student_id";
$assessments = mysqli_fetch_assoc(mysqli_query($conn, $assessment_query));

include 'includes/header.php';
?>

<div class="dashboard">
    <div class="welcome-card">
        <h2>Welcome, <?php echo htmlspecialchars($student['name']); ?></h2>
        <p><?php echo htmlspecialchars($student['course_class']); ?> | <?php echo htmlspecialchars($student['semester'] . ' ' . $student['academic_year']); ?></p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon">📖</div>
            <div class="stat-info">
                <h3><?php echo $entry_count['total']; ?></h3>
                <p>Logbook Entries</p>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-info">
                <h3><?php echo $submitted['total']; ?></h3>
                <p>Submitted</p>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📝</div>
            <div class="stat-info">
                <h3><?php echo $assessments['total']; ?></h3>
                <p>Assessments</p>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📁</div>
            <div class="stat-info">
                <h3><?php echo htmlspecialchars($student['project_title'] ?: 'Not Set'); ?></h3>
                <p>Project</p>
            </div>
        </div>
    </div>

    <div class="dashboard-grid">
        <div class="card">
            <div class="card-header">
                <h3>Project Details</h3>
            </div>
            <div class="card-body">
                <p><strong>Title:</strong> <?php echo htmlspecialchars($student['project_title'] ?: 'Not set'); ?></p>
                <p><strong>Technologies:</strong> <?php echo htmlspecialchars($student['technologies'] ?: 'Not set'); ?></p>
                <p><strong>Admission:</strong> <?php echo htmlspecialchars($student['admission_number']); ?></p>
                <p><strong>Lecturer:</strong> <?php echo htmlspecialchars($student['lecturer_name'] ?: 'Not set'); ?></p>
                <?php if ($student['portfolio_link']): ?>
                    <p><strong>Portfolio:</strong> <a href="<?php echo htmlspecialchars($student['portfolio_link']); ?>" target="_blank"><?php echo htmlspecialchars($student['portfolio_link']); ?></a></p>
                <?php endif; ?>
            </div>
        </div>
        <div class="card">
            <div class="card-header">
                <h3>Quick Actions</h3>
            </div>
            <div class="card-body">
                <a href="logbook.php" class="btn btn-primary btn-full">Add Logbook Entry</a>
                <a href="profile.php" class="btn btn-secondary btn-full" style="margin-top: 10px;">Update Profile</a>
                <a href="courses.php" class="btn btn-secondary btn-full" style="margin-top: 10px;">View Courses</a>
            </div>
        </div>
    </div>
</div>

<?php include 'includes/footer.php'; ?>

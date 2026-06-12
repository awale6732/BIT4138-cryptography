<?php
require_once 'includes/config.php';

if (!isset($_SESSION['student_id'])) {
    header('Location: index.php');
    exit();
}

$courses_query = "SELECT * FROM courses";
$courses_result = mysqli_query($conn, $courses_query);

$student_id = $_SESSION['student_id'];
$assessments_query = "SELECT a.*, c.unit_code, c.unit_name 
                      FROM assessments a 
                      JOIN courses c ON a.course_id = c.id 
                      WHERE a.student_id = $student_id";
$assessments_result = mysqli_query($conn, $assessments_query);

include 'includes/header.php';
?>

<div class="page-header">
    <h2>My Courses</h2>
</div>

<div class="course-list">
    <?php while ($course = mysqli_fetch_assoc($courses_result)): ?>
        <div class="course-card">
            <div class="course-code"><?php echo htmlspecialchars($course['unit_code']); ?></div>
            <div class="course-details">
                <h3><?php echo htmlspecialchars($course['unit_name']); ?></h3>
                <p class="lecturer">Lecturer: <?php echo htmlspecialchars($course['lecturer']); ?></p>
                <p><?php echo htmlspecialchars($course['description']); ?></p>
            </div>
        </div>
    <?php endwhile; ?>
</div>

<?php if (mysqli_num_rows($assessments_result) > 0): ?>
    <div class="card" style="margin-top: 20px;">
        <div class="card-header">
            <h3>My Assessment Scores</h3>
        </div>
        <div class="card-body">
            <table class="table">
                <thead>
                    <tr>
                        <th>Course</th>
                        <th>Assessment</th>
                        <th>Score</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    <?php while ($ass = mysqli_fetch_assoc($assessments_result)): ?>
                        <tr>
                            <td><?php echo htmlspecialchars($ass['unit_code']); ?></td>
                            <td><?php echo htmlspecialchars($ass['assessment_name']); ?></td>
                            <td><?php echo $ass['marks']; ?></td>
                            <td><?php echo $ass['total_marks']; ?></td>
                        </tr>
                    <?php endwhile; ?>
                </tbody>
            </table>
        </div>
    </div>
<?php endif; ?>

<?php include 'includes/footer.php'; ?>

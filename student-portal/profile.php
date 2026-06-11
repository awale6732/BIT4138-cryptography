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

$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = mysqli_real_escape_string($conn, $_POST['name']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $lecturer = mysqli_real_escape_string($conn, $_POST['lecturer_name']);
    $project_title = mysqli_real_escape_string($conn, $_POST['project_title']);
    $technologies = mysqli_real_escape_string($conn, $_POST['technologies']);
    $portfolio_link = mysqli_real_escape_string($conn, $_POST['portfolio_link']);

    $update = "UPDATE students SET 
        name = '$name',
        email = '$email',
        lecturer_name = '$lecturer',
        project_title = '$project_title',
        technologies = '$technologies',
        portfolio_link = '$portfolio_link'
        WHERE id = $student_id";

    if (mysqli_query($conn, $update)) {
        $message = 'Profile updated successfully';
        $_SESSION['student_name'] = $name;
        $student = mysqli_fetch_assoc(mysqli_query($conn, $query));
    } else {
        $message = 'Error updating profile';
    }
}

include 'includes/header.php';
?>

<div class="page-header">
    <h2>My Profile</h2>
</div>

<?php if ($message): ?>
    <div class="alert alert-success"><?php echo $message; ?></div>
<?php endif; ?>

<div class="card">
    <div class="card-header">
        <h3>Personal Information</h3>
    </div>
    <div class="card-body">
        <form method="POST" action="">
            <div class="form-row">
                <div class="form-group">
                    <label>Admission Number</label>
                    <input type="text" value="<?php echo htmlspecialchars($student['admission_number']); ?>" disabled class="input-disabled">
                </div>
                <div class="form-group">
                    <label>Course/Class</label>
                    <input type="text" value="<?php echo htmlspecialchars($student['course_class']); ?>" disabled class="input-disabled">
                </div>
            </div>
            <div class="form-group">
                <label for="name">Full Name</label>
                <input type="text" id="name" name="name" value="<?php echo htmlspecialchars($student['name']); ?>" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" value="<?php echo htmlspecialchars($student['email']); ?>" required>
            </div>
            <div class="form-group">
                <label for="lecturer_name">Lecturer Name</label>
                <input type="text" id="lecturer_name" name="lecturer_name" value="<?php echo htmlspecialchars($student['lecturer_name'] ?: ''); ?>">
            </div>
            <hr>
            <h4>Project Details</h4>
            <div class="form-group">
                <label for="project_title">Project Title</label>
                <input type="text" id="project_title" name="project_title" value="<?php echo htmlspecialchars($student['project_title'] ?: ''); ?>" placeholder="e.g. Smart E-Commerce Web Application">
            </div>
            <div class="form-group">
                <label for="technologies">Selected Technologies</label>
                <input type="text" id="technologies" name="technologies" value="<?php echo htmlspecialchars($student['technologies'] ?: ''); ?>" placeholder="e.g. PHP + MySQL">
            </div>
            <div class="form-group">
                <label for="portfolio_link">GitHub / Portfolio Link</label>
                <input type="url" id="portfolio_link" name="portfolio_link" value="<?php echo htmlspecialchars($student['portfolio_link'] ?: ''); ?>" placeholder="https://github.com/student/project">
            </div>
            <button type="submit" class="btn btn-primary">Update Profile</button>
        </form>
    </div>
</div>

<?php include 'includes/footer.php'; ?>

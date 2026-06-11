<?php
require_once 'includes/config.php';

if (!isset($_SESSION['student_id'])) {
    header('Location: index.php');
    exit();
}

$student_id = $_SESSION['student_id'];

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['save_entry'])) {
    $week_number = (int)$_POST['week_number'];
    $week_title = mysqli_real_escape_string($conn, $_POST['week_title']);
    $reflection = mysqli_real_escape_string($conn, $_POST['reflection']);
    $status = isset($_POST['submit_entry']) ? 'submitted' : 'draft';

    $check = "SELECT id FROM logbook_entries WHERE student_id = $student_id AND week_number = $week_number";
    $check_result = mysqli_query($conn, $check);

    if (mysqli_num_rows($check_result) > 0) {
        $entry = mysqli_fetch_assoc($check_result);
        $update = "UPDATE logbook_entries SET 
            week_title = '$week_title',
            reflection = '$reflection',
            status = '$status'
            WHERE id = {$entry['id']}";
        mysqli_query($conn, $update);
    } else {
        $insert = "INSERT INTO logbook_entries (student_id, week_number, week_title, reflection, status) 
                   VALUES ($student_id, $week_number, '$week_title', '$reflection', '$status')";
        mysqli_query($conn, $insert);
    }
}

$entries_query = "SELECT * FROM logbook_entries WHERE student_id = $student_id ORDER BY week_number";
$entries_result = mysqli_query($conn, $entries_query);

include 'includes/header.php';
?>

<div class="page-header">
    <h2>Weekly Logbook</h2>
    <button class="btn btn-primary" onclick="document.getElementById('newEntryForm').style.display='block'">New Entry</button>
</div>

<div id="newEntryForm" class="card" style="display: none; margin-bottom: 20px;">
    <div class="card-header">
        <h3>Add Logbook Entry</h3>
    </div>
    <div class="card-body">
        <form method="POST" action="">
            <div class="form-group">
                <label for="week_number">Week Number</label>
                <input type="number" id="week_number" name="week_number" min="1" max="14" required>
            </div>
            <div class="form-group">
                <label for="week_title">Week Title</label>
                <input type="text" id="week_title" name="week_title" placeholder="e.g. Local Environment Setup" required>
            </div>
            <div class="form-group">
                <label for="reflection">Student Reflection (Max 100 words)</label>
                <textarea id="reflection" name="reflection" rows="5" maxlength="1000" required></textarea>
                <small><span id="wordCount">0</span> words</small>
            </div>
            <button type="submit" name="save_entry" class="btn btn-primary">Save as Draft</button>
            <button type="submit" name="save_entry" class="btn btn-success" onclick="this.form.querySelector('input[name=submit_entry]').value='1'">Submit</button>
            <input type="hidden" name="submit_entry" value="">
        </form>
    </div>
</div>

<div class="logbook-list">
    <?php if (mysqli_num_rows($entries_result) > 0): ?>
        <?php while ($entry = mysqli_fetch_assoc($entries_result)): ?>
            <div class="logbook-card">
                <div class="logbook-header">
                    <span class="week-badge">Week <?php echo $entry['week_number']; ?></span>
                    <span class="status-badge status-<?php echo $entry['status']; ?>"><?php echo ucfirst($entry['status']); ?></span>
                </div>
                <h3><?php echo htmlspecialchars($entry['week_title']); ?></h3>
                <p class="reflection-text"><?php echo nl2br(htmlspecialchars($entry['reflection'])); ?></p>
                <small>Last updated: <?php echo $entry['updated_at']; ?></small>
            </div>
        <?php endwhile; ?>
    <?php else: ?>
        <div class="empty-state">
            <p>No logbook entries yet. Click "New Entry" to add your first weekly log.</p>
        </div>
    <?php endif; ?>
</div>

<script>
document.getElementById('reflection')?.addEventListener('input', function() {
    const words = this.value.trim() === '' ? 0 : this.value.trim().split(/\s+/).length;
    document.getElementById('wordCount').textContent = words;
});
</script>

<?php include 'includes/footer.php'; ?>

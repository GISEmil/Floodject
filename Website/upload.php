<?php
$target_dir = "C:/xampp/htdocs/";
$target_file = $target_dir . basename($_FILES["datafile"]["name"]);
$uploadOk = 1;
$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
// Check if image file is a actual image or fake image
if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["datafile"]["tmp_name"]);
    if($check !== false) {
        echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
}
// Check if file already exists
if (file_exists($target_file)) {
    echo "Sorry, file already exists.";
    $uploadOk = 0;
}

// Allow certain file formats
if($imageFileType != "tif") {
    echo "Sorry, only Tiff files are allowed.";
    $uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
	imagepng(imagecreatefromstring(file_get_contents($_FILES["datafile"]["name"])), "")
    if (move_uploaded_file($_FILES["datafile"]["tmp_name"], $target_file)) {
        echo "The file ". basename( $_FILES["datafile"]["name"]). " has been uploaded.";
		sleep(1);
		header("Location: Intro.html");
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}

?>

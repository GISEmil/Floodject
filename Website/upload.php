<?php

date_default_timezone_set('GMT');
$date = new DateTime();
$datestr = $date->format("zhms");
$target_dir = "/var/www/html/";
$target_dir2 = "/var/www/html/uploadpng/";
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
//Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
//if everything is ok, try to upload file
} else {
if (move_uploaded_file($_FILES["datafile"]["tmp_name"], $target_file)) {
	copy($target_file, $target_dir . "something.tif");
	rename($target_file, $datestr . ".tif");
	
	
	//imagepng($target_file2);
		//if ((move_uploaded_file($_FILES["datafile"]["tmp_name"], $target_file)) and (move_uploaded_file($target_file2, $target_dir))) {
	echo "The file ". basename( $_FILES["datafile"]["name"]). " has been uploaded and has been renamed to". $datestr;
	
	//rename($target_file2, $datestr . ".tif");
	
	imagepng($target_dir . "something.tif");
	rename($target_dir . "something.tif", $datestr . ".png");
	header("Location: second.html");
		}
	else {
		echo "Sorry, there was an error uploading your file.";
	}
}

?>

<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>Home</title>
    <link rel="stylesheet" type="text/css" href="css/ionicons.min.css">
    <link rel="stylesheet" type="text/css" href="css/index.css">
</head>
<body>
<div class="container">   

<div id='for-message'></div>

    <div class="centerInfo"><br><br><br> <br> 
      <h3 style="padding-top:25px;" >Lucrare de Licenta</h3><br>
      <h3>Detectarea COVID-19 utilizand Radiografia Toracica</h3>
    </div>

    <form  name='ourForm' method="post" enctype="multipart/form-data"><br><br><br>  
        <div class="dws-input">
          <input type="file" name="images" style="color:transparent; padding-left:250px;margin-bottom:10px;margin-top:-15px;"/>
        </div>     
        <button class="dws-submit" id="chooseFile"type="submit" name="Upload-Img" style="padding: 14.5px 133px;"><i style="font-size:22px;" class="ion-ios-paperplane"></i> Incarca Imaginea</button><br><br>    
        <button class="dws-submit" id="chooseFile" type="submit" name="GetRes" style="padding: 16px 128px;"><i class="ion-checkmark-circled"></i> Obtine Rezultatele</button><br><br><br> 
    </form>

</div>
</body>
</html>

<?php
//<div id='for-message'></div>
  exec('python Tools/removeImg.py');
  $flag = 0;
  if(isset($_POST["Upload-Img"]))
  {
    $img = $_FILES["images"]["name"];
    $img_loc = $_FILES["images"]["tmp_name"];
    $img_folder = "Image/";

    if(move_uploaded_file($img_loc,$img_folder.$img))
    {
      exec('python Tools/predict.py');
      $flag = 1;
    }
  }

  if ($flag>0){
    //echo "tot ok ";
    ?>
      <script>
      var serverResponse = document.querySelector('#for-message');

      document.forms.ourForm.onsubmit = function(e){
          e.preventDefault();   
          
          var xhr = new XMLHttpRequest();

          xhr.open('POST', 'Tools/redirect.php');

          var formData =  new FormData(document.forms.ourForm);

          xhr.onreadystatechange = function()
          {
              if(xhr.readyState===4 && xhr.status===200)
              {
                  serverResponse.textContent = xhr.responseText;
                  serverResponse.textContent.replace("\n", "");
                  serverResponse.textContent.trim();
                  console.log(serverResponse.textContent);

                  if(serverResponse.textContent==="")
                  {
                    location.href='Chart/chart.php';                
                  }
              }
          }
          xhr.send(formData);
      };
      </script>

<?php
  }
?>


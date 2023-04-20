import { Component, OnInit } from '@angular/core';
import { lastValueFrom, map, Observable } from 'rxjs';
import { RESTAPIServiceService } from '../restapiservice.service';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {

  constructor(private __apiservice: RESTAPIServiceService) { }

  ngOnInit(): void { }

  fileName = ''
  imageSrcBefore: any
  imageSrcAfter: any
  file: any
  srcImage: any
  recieved = false
  images: any
  image1: any
  image2: any
  u: boolean = true

  sent = false

  fileUrl = ''

  setBeforeImg(event: any): void {
      if (event.target!.files && event.target!.files[0]) {
        this.file = event.target.files[0];
        this.fileName = this.file.name 
        this.image1 = this.file
        var reader = new FileReader();
        reader.onload = e => this.imageSrcBefore = reader.result;
        reader.readAsDataURL(this.file);
    }
  }

  setAfterImg(event: any): void {
    if (event.target!.files && event.target!.files[0]) {
      this.file = event.target.files[0];
      this.fileName = this.file.name 
      this.image2 = this.file
      var reader = new FileReader();
      reader.onload = e => this.imageSrcAfter = reader.result;
      reader.readAsDataURL(this.file);
    }
  }

  mainUpload() {
    const formData = new FormData();
    formData.append('image1', this.image1);
    formData.append('image2', this.image2);
    this.__apiservice.uploadImage(formData)
    this.sent = true
  }

  getUp() {
    this.__apiservice.getUploadedImages().subscribe( (data: any) => {
      this.images = data
      this.recieved = true
      this.u = false
    })
  }


}

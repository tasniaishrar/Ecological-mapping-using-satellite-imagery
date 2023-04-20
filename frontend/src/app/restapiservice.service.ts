import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpRequest } from '@angular/common/http'
import { Observable, throwError } from 'rxjs';
import { catchError, map, retry } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class RESTAPIServiceService {

  constructor(private http: HttpClient) { }

  baseUrl = 'http://127.0.0.1:8000/api/add/?';
  uploadedImageUrl = 'http://127.0.0.1:8000/api/getUp/'
  imagePostUrl = 'http://127.0.0.1:8000/api/upload/'
  imageUrl = ''
  resp: any

  getImages(x:any, y:any): any {
    this.imageUrl = ''
    this.imageUrl = this.baseUrl +'x=' + x + '&y=' + y
    console.log(this.imageUrl)
    return this.http.get(this.imageUrl);
  }

  getUploadedImages() {
    return this.http.get(this.uploadedImageUrl)
  }

  uploadImage(formData: any): any {
      this.http.post(this.imagePostUrl, formData).subscribe( r => {
        console.log(r)
      })
  }
}

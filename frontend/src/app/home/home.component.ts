import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  h: boolean = true
  showMap: boolean = false
  showUpload: boolean = false
  back:any
  dispDat: any
  dispShow = false

  map() {
    if (this.showUpload == true) {
      this.showUpload = false
    }
    this.showMap = true
    this.dispShow = false
    this.h = false
  }

  upload() {
    if (this.showMap == true) {
      this.showMap = false
    }
    this.showUpload = true
    this.dispShow=false
    this.h = false
  }

  nav(back: any) {
    if (back=="home") {
      this.h = true
    }
    else if (back=="map"){
      this.map()
      // this.dispShow = true
    }
    else if (back == "upload") {
      this.upload()
    } 
  }

  showDisp(ev: any){
    this.dispDat = ev
    this.showMap = false
    this.h=false
    this.showUpload=false
    this.dispShow = true
  }
}

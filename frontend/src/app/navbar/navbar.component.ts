import { Component, EventEmitter, Input, Output} from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {

  @Input() h: any

  @Output() back = new EventEmitter<string>();

  checker:string = ""

  goMap() {
    this.checker = "map"
    this.back.emit(this.checker);
  }

  goUpload() {
    this.checker = "upload"
    this.back.emit(this.checker);
  }
  
  goBack() {
    this.checker = "home"
    this.back.emit(this.checker);
  }
}

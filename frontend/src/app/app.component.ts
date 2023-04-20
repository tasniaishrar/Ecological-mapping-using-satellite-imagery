import { Component } from '@angular/core';
import { RESTAPIServiceService } from './restapiservice.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private __apiservice: RESTAPIServiceService) { }
  ngOnInit() {}
}

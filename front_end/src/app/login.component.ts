import {Component} from "@angular/core";
import {WebService} from "./web.service";
import {FormBuilder, Validators} from "@angular/forms";
import { Router } from '@angular/router';


@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent {
  gov_id: any;
  password: any;

  constructor(private webService: WebService, private router: Router) {}

  onSubmit() {
    this.webService.login({ gov_id: this.gov_id, password: this.password }).subscribe(
      () => {
        console.log('Login successful');
        this.router.navigate(['/profile']);
      },
      (error: any) => {
        console.error('Login failed:', error);
      }
    );
  }
}

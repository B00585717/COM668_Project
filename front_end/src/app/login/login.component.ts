import { Component } from '@angular/core';
import {WebService} from "../web.service";
import {Router} from '@angular/router';
import {AuthService} from '../auth.service';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  gov_id: any;
  password: any;
  loggedInUserData: any;

  constructor(private webService: WebService, private router: Router, private authService: AuthService) {}

  onSubmit() {
    this.webService.login({ gov_id: this.gov_id, password: this.password }).subscribe(
      (response: any) => {
        console.log('Login successful');
        const loggedInUserData = response.user_data;
        sessionStorage.setItem('access_token', response.access_token);
        this.authService.setLoggedIn(true);
        this.router.navigate(['/profile']);
        this.authService.setUser(loggedInUserData);
      },
      (error: any) => {
        console.error('Login failed:', error);
      }
    );
  }
}

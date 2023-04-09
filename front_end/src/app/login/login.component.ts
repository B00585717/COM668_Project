import { Component } from '@angular/core';
import {WebService} from "../services/web.service";
import {Router} from '@angular/router';
import {AuthService} from '../services/auth.service';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  gov_id: any;
  password: any;

  constructor(private webService: WebService, private router: Router, private authService: AuthService) {}

  onSubmit() {
    this.webService.login({ gov_id: this.gov_id, password: this.password }).subscribe(
      (response: any) => {
        const loggedInUserData = response.user_data;

        this.authService.setLoggedIn(true);
        this.authService.setUser(loggedInUserData);
        this.router.navigate(['/profile']);

        sessionStorage.setItem('access_token', response.access_token);
      },
      (error: any) => {
        console.error('Login failed:', error);
      }
    );
  }
}

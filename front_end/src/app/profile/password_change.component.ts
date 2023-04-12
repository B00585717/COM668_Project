import { Component } from '@angular/core';
import { WebService } from '../services/web.service';
import { AuthService } from '../services/auth.service';
import {Router} from "@angular/router";

@Component({
  selector: 'password_change',
  templateUrl: './password_change.component.html',
  styleUrls: ['password_change.component.css'],
})
export class Password_changeComponent {
  newPassword: any;
  email: any;

  constructor(private webService: WebService,
              private authService: AuthService,
              private router: Router) {}

  updatePassword() {
    const g_id = this.authService.getGovId();
    console.log(this.authService.getGovId())
    this.webService.updatePassword(g_id, this.email, this.newPassword).subscribe(
      (response) => {
        this.router.navigate(['/profile']);
        console.log('Password successfully updated:', response);
      },
      (error) => {
        console.error('Error updating password:', error);
      }
    );
  }
}

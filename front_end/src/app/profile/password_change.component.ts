import { Component } from '@angular/core';
import { WebService } from '../web.service';
import { AuthService } from '../auth.service';

@Component({
  selector: 'password_change',
  templateUrl: './password_change.component.html',
  styleUrls: ['password_change.component.css'],
})
export class Password_changeComponent {
  newPassword: any;

  constructor(private webService: WebService, private authService: AuthService) {}

  updatePassword() {
    const g_id = this.authService.getUser().gov_id;
    this.webService.updatePassword(g_id, this.newPassword).subscribe(
      (response) => {
        console.log('Password successfully updated:', response);
      },
      (error) => {
        console.error('Error updating password:', error);
      }
    );
  }
}

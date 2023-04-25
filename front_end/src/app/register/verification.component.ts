import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import {FormBuilder, Validators} from "@angular/forms";
import { EmailService } from '../services/email.service';

@Component({
  selector: 'verification',
  templateUrl: 'verification.component.html',
  styleUrls: ['./verification.component.css']
})
export class VerificationComponent {
  email: any;
  verificationForm: any;
  email_regex = '\\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}\\b'

  constructor(private http: HttpClient,
              private router: Router,
              private formBuilder: FormBuilder,
              private emailService: EmailService) {}

  ngOnInit(){
    this.verificationForm = this.formBuilder.group({
      email: ['', Validators.pattern(this.email_regex)],
  });
  }
  sendOtp() {
    this.email = this.verificationForm.get('email').value; // Add this line to get the email value
    this.http
        .post('http://localhost:5000/api/v1.0/verification', { email: this.email })
        .subscribe(
          () => {
            this.emailService.setEmail(this.email);
            this.router.navigate(['/register']);
          },
          (error) => {
            console.error('Error sending OTP:', error);
          }
    );
  }
}

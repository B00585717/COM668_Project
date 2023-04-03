import {Component} from "@angular/core";
import {WebService} from "./web.service";
import {FormBuilder, Validators} from "@angular/forms";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent {

  loginForm: any;

  constructor(public webService: WebService, private route: ActivatedRoute, private formBuilder: FormBuilder) {
  }
  ngOnInit() {

    this.loginForm = this.formBuilder.group({
      gov_id: ['', Validators.required],
      password: ['', Validators.required],

    });
  }

  onSubmit() {
    //console log for testing
    console.log(this.loginForm.value);
    this.webService.login(this.loginForm.value).subscribe((response: any) => {
      this.loginForm.reset();
    });
  }
}

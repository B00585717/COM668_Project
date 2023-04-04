import {Component} from "@angular/core";
import {FormBuilder} from "@angular/forms";
import {ActivatedRoute} from "@angular/router";
import {WebService} from "../web.service";

@Component({
  selector: 'candidate',
  templateUrl: './candidate.component.html',
  styleUrls: ['./candidate.component.css']
})

export class CandidateComponent {

  candidate_list: any = [];

  candidate_form: any;

  constructor(public webService: WebService, private route: ActivatedRoute, private formBuilder: FormBuilder) {
  }

  ngOnInit() {
    this.candidate_list = this.webService.getCandidate(this.route.snapshot.params['id']);

  }
  onSubmit() {
    this.webService.updateCandidate(this.candidate_form.value).subscribe((response: any) => {
      this.candidate_form.reset();
    });

    this.candidate_form = this.formBuilder.group({
      candidate_firstname: this.candidate_list.candidate_firstname,
      candidate_lastname: '',
      party_id: '',
      image: '',
      constituency_id: '',
      statement:'',
    });
  }
}

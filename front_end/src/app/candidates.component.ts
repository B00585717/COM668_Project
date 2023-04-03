import {Component} from "@angular/core";
import {WebService} from "./web.service";
import {FormBuilder} from "@angular/forms";
import { ActivatedRoute } from "@angular/router";

@Component({
  selector: 'candidates',
  templateUrl: './candidates.component.html',
  styleUrls: ['./candidates.component.css']
})

export class CandidatesComponent {

  candidate_list: any = [];
  party_list: any = [];

  candidate_form: any;
  party: any;


  constructor(public webService: WebService, private route: ActivatedRoute, private formBuilder: FormBuilder) {
  }

  ngOnInit() {
    this.candidate_list = this.webService.getCandidates();
  }

  onSubmit() {
    this.webService.addCandidate(this.candidate_form.value).subscribe((response: any) => {
      this.candidate_form.reset();
    });

    this.candidate_form = this.formBuilder.group({
      candidate_firstname: '',
      candidate_lastname: '',
      party_id: '',
      image: '',
      constituency_id: '',
      statement:'',
    });

    this.candidate_list = this.webService.getCandidates();
  }
}

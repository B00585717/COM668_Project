import {Component} from "@angular/core";
import {WebService} from "../web.service";
import {FormBuilder} from "@angular/forms";
import { ActivatedRoute } from "@angular/router";
import {VoteService} from "../vote.service";
import { AuthService } from '../auth.service';

@Component({
  selector: 'candidates',
  templateUrl: './candidates.component.html',
  styleUrls: ['./candidates.component.css']
})

export class CandidatesComponent {

  candidate_list: any = [];
  candidate_form: any;

  voter_id: any;

  constructor(public webService: WebService, private route: ActivatedRoute, private formBuilder: FormBuilder, private voteService: VoteService, private authService: AuthService) {
    const user = this.authService.getUser();
    this.voter_id = user ? user.voter_id : null;
  }

  onVoteButtonClick(candidate_id: number) {
    console.log('Voter ID:', this.voter_id);
    console.log('Candidate ID:', candidate_id);
    this.voteService.voteForCandidate(this.voter_id, candidate_id).subscribe(
      response => console.log('Vote submitted', response),
      error => console.error('Error submitting vote', error)
    );
  }

  ngOnInit() {
    this.candidate_list = this.webService.getCandidates();
    this.voter_id = this.authService.getUser().voter_id;
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
  }
}
